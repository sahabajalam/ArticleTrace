"""JSON-backed vector store for semantic search over KG entities.

Uses cosine similarity for search, stores embeddings in JSON files.
No external server dependency (ChromaDB incompatible with Python 3.14).

Collections:
  - articles: GDPR + AI Act articles
  - recitals: Recital text
  - interpretive: Guidelines, CaseLaw, Enforcement
  - definitions: Definition text
  - obligations: Obligation/Exemption text

Each collection is a JSON file in the persist directory.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


class VectorStore:
    """File-backed vector store with cosine similarity search."""

    COLLECTIONS = [
        "articles",
        "recitals",
        "interpretive",
        "definitions",
        "obligations",
        "concepts",
        "rights",
    ]

    def __init__(self, persist_dir: str):
        self._dir = Path(persist_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        self._cache: dict[str, dict] = {}

    def _collection_path(self, name: str) -> Path:
        return self._dir / f"{name}.json"

    def _load_collection(self, name: str) -> dict:
        """Load collection data from disk."""
        if name in self._cache:
            return self._cache[name]

        path = self._collection_path(name)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
        else:
            data = {"ids": [], "documents": [], "embeddings": [], "metadatas": []}

        self._cache[name] = data
        return data

    def _save_collection(self, name: str) -> None:
        """Save collection to disk."""
        data = self._cache.get(name, {})
        path = self._collection_path(name)
        path.write_text(
            json.dumps(data, ensure_ascii=False),
            encoding="utf-8",
        )

    def add_documents(
        self,
        collection_name: str,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, Any]],
        batch_size: int = 100,
    ) -> int:
        """Add documents with pre-computed embeddings."""
        data = self._load_collection(collection_name)

        # Build existing ID set for dedup
        existing_ids = set(data["ids"])

        added = 0
        for i in range(len(ids)):
            if ids[i] not in existing_ids:
                data["ids"].append(ids[i])
                data["documents"].append(documents[i])
                data["embeddings"].append(embeddings[i])
                # Clean metadata
                clean_meta = {}
                for k, v in metadatas[i].items():
                    if v is not None:
                        clean_meta[k] = v if isinstance(v, (str, int, float, bool)) else str(v)
                data["metadatas"].append(clean_meta)
                existing_ids.add(ids[i])
                added += 1

        self._save_collection(collection_name)
        return added

    def query(
        self,
        collection_name: str,
        query_embedding: list[float],
        n_results: int = 10,
        where: dict | None = None,
    ) -> dict:
        """Query collection with cosine similarity."""
        data = self._load_collection(collection_name)

        if not data["ids"]:
            return {"ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]}

        # Compute cosine similarities
        scores: list[tuple[int, float]] = []
        for idx, emb in enumerate(data["embeddings"]):
            # Apply metadata filter if provided
            if where:
                meta = data["metadatas"][idx]
                if not self._matches_filter(meta, where):
                    continue

            sim = self._cosine_similarity(query_embedding, emb)
            # Distance = 1 - similarity (lower = more similar)
            scores.append((idx, 1.0 - sim))

        # Sort by distance (ascending)
        scores.sort(key=lambda x: x[1])
        top = scores[:n_results]

        result_ids = [data["ids"][i] for i, _ in top]
        result_docs = [data["documents"][i] for i, _ in top]
        result_metas = [data["metadatas"][i] for i, _ in top]
        result_dists = [d for _, d in top]

        return {
            "ids": [result_ids],
            "documents": [result_docs],
            "metadatas": [result_metas],
            "distances": [result_dists],
        }

    def count(self, collection_name: str) -> int:
        """Count documents in collection."""
        data = self._load_collection(collection_name)
        return len(data["ids"])

    def delete_collection(self, name: str) -> None:
        """Delete a collection."""
        path = self._collection_path(name)
        if path.exists():
            path.unlink()
        self._cache.pop(name, None)

    def clear_all(self) -> None:
        """Delete all collections."""
        for name in self.COLLECTIONS:
            self.delete_collection(name)

    @staticmethod
    def _cosine_similarity(a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    @staticmethod
    def _matches_filter(meta: dict, where: dict) -> bool:
        """Check if metadata matches a simple filter.

        Supports: {"field": "value"} for exact match.
        """
        for key, value in where.items():
            if key.startswith("$"):
                continue  # Skip operators for now
            if meta.get(key) != value:
                return False
        return True
