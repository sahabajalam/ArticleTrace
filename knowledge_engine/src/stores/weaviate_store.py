"""Weaviate-backed vector store for semantic search over KG entities.

Preserves the exact public interface of `VectorStore` (JSON version) so
callers (retrieval engine, API, scripts) don't need to change.

Each collection name (articles, recitals, …) maps to a capitalised
Weaviate class (Articles, Recitals, …). Embeddings are supplied by the
caller — Weaviate's vectorizer is set to `none`. Metadata is stored as a
JSON-encoded string plus a first-class `regulation_id` for fast filtering.
"""

from __future__ import annotations

import json
from typing import Any

import weaviate
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.data import DataObject
from weaviate.classes.query import Filter, MetadataQuery


class WeaviateVectorStore:
    """Weaviate-backed vector store, interface-compatible with VectorStore."""

    COLLECTIONS = [
        "articles",
        "recitals",
        "interpretive",
        "definitions",
        "obligations",
        "concepts",
        "rights",
    ]

    def __init__(
        self,
        host: str = "localhost",
        http_port: int = 8080,
        grpc_port: int = 50051,
        persist_dir: str | None = None,  # accepted for interface parity, ignored
    ):
        self._host = host
        self._http_port = http_port
        self._grpc_port = grpc_port
        self._client: weaviate.WeaviateClient | None = None
        # Ensure schema exists for all known collections.
        self._ensure_schema()

    # ── Connection management ─────────────────────────────────────────────

    def _connect(self) -> weaviate.WeaviateClient:
        if self._client is None or not self._client.is_connected():
            self._client = weaviate.connect_to_local(
                host=self._host,
                port=self._http_port,
                grpc_port=self._grpc_port,
            )
        return self._client

    def close(self) -> None:
        if self._client is not None and self._client.is_connected():
            self._client.close()
            self._client = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    # ── Schema ────────────────────────────────────────────────────────────

    @staticmethod
    def _class_name(collection: str) -> str:
        """Map a collection name ('articles') to a Weaviate class ('Articles')."""
        return collection[:1].upper() + collection[1:]

    def _ensure_schema(self) -> None:
        client = self._connect()
        existing = {c.lower() for c in client.collections.list_all().keys()}
        for coll in self.COLLECTIONS:
            cls = self._class_name(coll)
            if cls.lower() in existing:
                continue
            client.collections.create(
                name=cls,
                vectorizer_config=Configure.Vectorizer.none(),
                properties=[
                    Property(name="entity_id", data_type=DataType.TEXT),
                    Property(name="document", data_type=DataType.TEXT),
                    Property(name="regulation_id", data_type=DataType.TEXT),
                    Property(name="metadata_json", data_type=DataType.TEXT),
                ],
            )

    # ── Writes ────────────────────────────────────────────────────────────

    def add_documents(
        self,
        collection_name: str,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        batch_size: int = 100,
    ) -> int:
        """Insert new documents. Skips ids already present (dedup by entity_id)."""
        client = self._connect()
        coll = client.collections.get(self._class_name(collection_name))

        existing_ids = self._existing_ids(coll, ids)
        to_insert: list[DataObject] = []
        for i, doc_id in enumerate(ids):
            if doc_id in existing_ids:
                continue
            meta = metadatas[i] or {}
            clean_meta = {
                k: (v if isinstance(v, (str, int, float, bool)) else str(v))
                for k, v in meta.items()
                if v is not None
            }
            to_insert.append(
                DataObject(
                    properties={
                        "entity_id": doc_id,
                        "document": documents[i],
                        "regulation_id": str(clean_meta.get("regulation_id", "")),
                        "metadata_json": json.dumps(clean_meta, ensure_ascii=False),
                    },
                    vector=list(embeddings[i]),
                )
            )

        added = 0
        for start in range(0, len(to_insert), batch_size):
            chunk = to_insert[start : start + batch_size]
            coll.data.insert_many(chunk)
            added += len(chunk)
        return added

    @staticmethod
    def _existing_ids(coll, ids: list[str]) -> set[str]:
        """Return the subset of `ids` that already exist in the collection."""
        if not ids:
            return set()
        found: set[str] = set()
        # Weaviate filters with an IN-style list over equal clauses
        for start in range(0, len(ids), 500):
            chunk = ids[start : start + 500]
            flt = Filter.by_property("entity_id").contains_any(chunk)
            resp = coll.query.fetch_objects(
                filters=flt,
                limit=len(chunk),
                return_properties=["entity_id"],
            )
            for obj in resp.objects:
                eid = obj.properties.get("entity_id")
                if isinstance(eid, str):
                    found.add(eid)
        return found

    # ── Queries ───────────────────────────────────────────────────────────

    def query(
        self,
        collection_name: str,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict | None = None,
    ) -> dict:
        """Vector search. Returns ChromaDB-style nested-list response."""
        client = self._connect()
        coll = client.collections.get(self._class_name(collection_name))

        flt = self._build_filter(where)
        resp = coll.query.near_vector(
            near_vector=list(query_embedding),
            limit=n_results,
            filters=flt,
            return_metadata=MetadataQuery(distance=True),
            return_properties=["entity_id", "document", "metadata_json", "regulation_id"],
        )

        ids: list[str] = []
        docs: list[str] = []
        metas: list[dict[str, Any]] = []
        dists: list[float] = []
        for obj in resp.objects:
            props = obj.properties
            ids.append(str(props.get("entity_id", "")))
            docs.append(str(props.get("document", "")))
            meta_raw = props.get("metadata_json") or "{}"
            try:
                metas.append(json.loads(meta_raw))
            except json.JSONDecodeError:
                metas.append({})
            dist = obj.metadata.distance if obj.metadata else None
            dists.append(float(dist) if dist is not None else 1.0)

        return {
            "ids": [ids],
            "documents": [docs],
            "metadatas": [metas],
            "distances": [dists],
        }

    @staticmethod
    def _build_filter(where: dict | None) -> Filter | None:
        if not where:
            return None
        clauses: list[Filter] = []
        for key, value in where.items():
            if key.startswith("$"):
                continue
            if key == "regulation_id":
                clauses.append(Filter.by_property("regulation_id").equal(str(value)))
            else:
                # Fallback: substring match in serialised metadata
                clauses.append(
                    Filter.by_property("metadata_json").like(f'*"{key}": "{value}"*')
                )
        if not clauses:
            return None
        if len(clauses) == 1:
            return clauses[0]
        return Filter.all_of(clauses)

    # ── Admin ─────────────────────────────────────────────────────────────

    def count(self, collection_name: str) -> int:
        client = self._connect()
        coll = client.collections.get(self._class_name(collection_name))
        return coll.aggregate.over_all(total_count=True).total_count or 0

    def delete_collection(self, name: str) -> None:
        client = self._connect()
        cls = self._class_name(name)
        if client.collections.exists(cls):
            client.collections.delete(cls)

    def clear_all(self) -> None:
        for name in self.COLLECTIONS:
            self.delete_collection(name)
        self._ensure_schema()
