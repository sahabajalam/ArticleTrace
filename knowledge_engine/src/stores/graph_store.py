"""Neo4j graph store for the EU AI Regulatory Knowledge Graph.

Fixes the core_2 _record_to_entity() roundtrip bug by using entity_from_dict()
to return proper subclass instances. Adds batch operations for loading 2000+ nodes.
"""

from __future__ import annotations

import logging
import re
from contextlib import contextmanager
from typing import Any, Generator

from neo4j import GraphDatabase, Driver, Session, ManagedTransaction

from ..schema.entities import Entity, EntityType, ENTITY_TYPE_MAP, entity_from_dict
from ..schema.relationships import Relationship, RelationshipType

logger = logging.getLogger(__name__)


class GraphStore:
    """Neo4j-backed knowledge graph store."""

    def __init__(self, uri: str, user: str, password: str):
        self._driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        self._verify_connection()

    def close(self) -> None:
        self._driver.close()

    def _verify_connection(self) -> None:
        """Verify Neo4j is reachable."""
        self._driver.verify_connectivity()
        logger.info("Connected to Neo4j")

    @contextmanager
    def _session(self) -> Generator[Session, None, None]:
        with self._driver.session() as session:
            yield session

    # ── Index management ──────────────────────────────────────────────────

    VECTOR_INDEX_NAME = "entity_embedding"
    VECTOR_DIMENSIONS = 3072  # gemini-embedding-001
    VECTOR_COLLECTIONS = [
        "articles",
        "recitals",
        "interpretive",
        "definitions",
        "obligations",
        "concepts",
        "rights",
    ]

    def create_indexes(self) -> None:
        """Create indexes for all entity types on id and type fields."""
        with self._session() as session:
            # Composite index on id (unique across all nodes)
            session.run(
                "CREATE CONSTRAINT entity_id IF NOT EXISTS "
                "FOR (n:Entity) REQUIRE n.id IS UNIQUE"
            )
            # Index per entity type label for fast lookups
            for entity_type in EntityType:
                label = entity_type.value
                session.run(
                    f"CREATE INDEX idx_{label.lower()}_id IF NOT EXISTS "
                    f"FOR (n:{label}) ON (n.id)"
                )
            logger.info("Indexes created for all entity types")

    def create_vector_index(self) -> None:
        """Create the Neo4j-native vector index over :Entity(embedding).

        One index covers all 7 collections; queries filter by `n.collection`.
        """
        with self._session() as session:
            session.run(
                f"CREATE VECTOR INDEX {self.VECTOR_INDEX_NAME} IF NOT EXISTS "
                f"FOR (n:Entity) ON (n.embedding) "
                f"OPTIONS {{indexConfig: {{"
                f"  `vector.dimensions`: {self.VECTOR_DIMENSIONS}, "
                f"  `vector.similarity_function`: 'cosine'"
                f"}}}}"
            )
            logger.info("Vector index created: %s", self.VECTOR_INDEX_NAME)

    def vector_index_exists(self) -> bool:
        """Return True if the vector index is present and ONLINE."""
        with self._session() as session:
            result = session.run(
                "SHOW VECTOR INDEXES YIELD name, state "
                "WHERE name = $name RETURN state",
                name=self.VECTOR_INDEX_NAME,
            )
            record = result.single()
            return bool(record and record["state"] == "ONLINE")

    def vector_collection_counts(self) -> dict[str, int]:
        """Return embedding counts per collection — used by /health."""
        counts: dict[str, int] = {c: 0 for c in self.VECTOR_COLLECTIONS}
        with self._session() as session:
            result = session.run(
                "MATCH (n:Entity) WHERE n.embedding IS NOT NULL "
                "RETURN n.collection AS collection, count(n) AS cnt"
            )
            for record in result:
                coll = record["collection"]
                if coll in counts:
                    counts[coll] = record["cnt"]
        return counts

    # ── Vector search ─────────────────────────────────────────────────────

    def vector_search(
        self,
        query_embedding: list[float],
        n_results: int = 10,
        collections: list[str] | None = None,
        regulation_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """Vector similarity search over :Entity nodes.

        Returns list of dicts with id, document, metadata, similarity (0-1),
        ready for the retrieval engine's RRF fusion.
        """
        # The vector index returns top-N globally; we over-fetch then filter.
        candidate_k = max(n_results * 4, 50)

        params: dict[str, Any] = {
            "k": candidate_k,
            "embedding": query_embedding,
        }
        where_clauses: list[str] = []
        if collections:
            where_clauses.append("node.collection IN $collections")
            params["collections"] = collections
        if regulation_filter:
            where_clauses.append("node.regulation_id = $regulation")
            params["regulation"] = regulation_filter

        where_sql = ""
        if where_clauses:
            where_sql = "WHERE " + " AND ".join(where_clauses)

        query = (
            f"CALL db.index.vector.queryNodes('{self.VECTOR_INDEX_NAME}', $k, $embedding) "
            f"YIELD node, score "
            f"{where_sql} "
            f"RETURN node, score "
            f"ORDER BY score DESC "
            f"LIMIT $top_k"
        )
        params["top_k"] = n_results

        results: list[dict[str, Any]] = []
        with self._session() as session:
            for record in session.run(query, **params):
                node = record["node"]
                node_dict = self._node_to_dict(node)
                results.append({
                    "entity_id": node_dict.get("id", ""),
                    "collection": node_dict.get("collection", ""),
                    "document": node_dict.get("document_text") or self._derive_document(node_dict),
                    "metadata": self._derive_metadata(node_dict),
                    "similarity": float(record["score"]),
                })
        return results

    @staticmethod
    def _derive_document(node: dict[str, Any]) -> str:
        """Pick the best text field for retrieval results.

        Articles/Recitals carry `full_text`; Obligations carry `document` or
        `text`; Definitions carry `definition_text`. Falls back to name/title.
        """
        for key in ("document", "full_text", "text", "definition_text", "description"):
            val = node.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return node.get("title") or node.get("name") or ""

    @staticmethod
    def _derive_metadata(node: dict[str, Any]) -> dict[str, Any]:
        """Build the metadata dict the retrieval engine consumes."""
        return {
            "entity_id": node.get("id", ""),
            "type": node.get("type", ""),
            "regulation_id": node.get("regulation_id", ""),
            "article_number": node.get("article_number", ""),
            "article_reference": node.get("article_reference", ""),
        }

    # ── Node operations ───────────────────────────────────────────────────

    def create_node(self, entity: Entity | dict[str, Any]) -> None:
        """Create a single node from an Entity or dict."""
        if isinstance(entity, dict):
            props = entity
            entity_type = props.get("type", "Entity")
        else:
            props = entity.model_dump(mode="json", exclude_none=True)
            entity_type = entity.type.value

        # Flatten provenance into top-level properties for Cypher
        provenance = props.pop("provenance", {})
        for k, v in provenance.items():
            props[f"prov_{k}"] = v

        # Neo4j can't store dicts/lists of dicts as properties — serialize complex fields
        for key in list(props.keys()):
            val = props[key]
            if isinstance(val, dict):
                import json
                props[key] = json.dumps(val, default=str)
            elif isinstance(val, list) and val and isinstance(val[0], dict):
                import json
                props[key] = json.dumps(val, default=str)

        label = entity_type if isinstance(entity_type, str) else entity_type.value
        with self._session() as session:
            session.run(
                f"MERGE (n:Entity:{label} {{id: $id}}) SET n += $props",
                id=props["id"],
                props=props,
            )

    def create_nodes_batch(
        self, entities: list[dict[str, Any]], batch_size: int = 500
    ) -> int:
        """Batch create nodes. Returns count of nodes created."""
        total = 0
        for i in range(0, len(entities), batch_size):
            batch = entities[i : i + batch_size]
            self._create_batch(batch)
            total += len(batch)
            logger.info(f"  Created {total}/{len(entities)} nodes")
        return total

    def _create_batch(self, entities: list[dict[str, Any]]) -> None:
        """Create a batch of nodes in a single transaction."""
        import json

        def _tx_func(tx: ManagedTransaction, batch: list[dict]) -> None:
            for props in batch:
                entity_type = props.get("type", "Entity")
                label = entity_type if isinstance(entity_type, str) else entity_type

                # Flatten provenance
                provenance = props.pop("provenance", {}) if "provenance" in props else {}
                clean_props = {}
                for k, v in props.items():
                    if isinstance(v, dict):
                        clean_props[k] = json.dumps(v, default=str)
                    elif isinstance(v, list) and v and isinstance(v[0], dict):
                        clean_props[k] = json.dumps(v, default=str)
                    else:
                        clean_props[k] = v
                for k, v in provenance.items():
                    clean_props[f"prov_{k}"] = str(v) if v is not None else None

                tx.run(
                    f"MERGE (n:Entity:{label} {{id: $id}}) SET n += $props",
                    id=clean_props["id"],
                    props=clean_props,
                )

        with self._session() as session:
            session.execute_write(_tx_func, entities)

    # ── Relationship operations ───────────────────────────────────────────

    def create_relationship(self, rel: Relationship | dict[str, Any]) -> None:
        """Create a single relationship."""
        if isinstance(rel, dict):
            source_id = rel["source_id"]
            target_id = rel["target_id"]
            rel_type = rel["type"]
            props = rel.get("properties", {})
        else:
            source_id = rel.source_id
            target_id = rel.target_id
            rel_type = rel.type.value if isinstance(rel.type, RelationshipType) else rel.type
            props = rel.properties

        with self._session() as session:
            session.run(
                f"MATCH (a:Entity {{id: $source_id}}) "
                f"MATCH (b:Entity {{id: $target_id}}) "
                f"MERGE (a)-[r:{rel_type}]->(b) SET r += $props",
                source_id=source_id,
                target_id=target_id,
                props=props,
            )

    def create_relationships_batch(
        self, rels: list[dict[str, Any]], batch_size: int = 500
    ) -> tuple[int, int]:
        """Batch create relationships. Returns (created, skipped) counts."""
        created = 0
        skipped = 0

        for i in range(0, len(rels), batch_size):
            batch = rels[i : i + batch_size]
            batch_created, batch_skipped = self._create_rel_batch(batch)
            created += batch_created
            skipped += batch_skipped
            logger.info(f"  Relationships: {created + skipped}/{len(rels)} processed ({skipped} skipped)")

        return created, skipped

    def _create_rel_batch(self, rels: list[dict[str, Any]]) -> tuple[int, int]:
        """Create a batch of relationships in a single transaction."""
        created = 0
        skipped = 0

        def _tx_func(tx: ManagedTransaction, batch: list[dict]) -> tuple[int, int]:
            nonlocal created, skipped
            for rel in batch:
                source_id = rel["source_id"]
                target_id = rel["target_id"]
                rel_type = rel["type"]
                props = rel.get("properties", {})

                result = tx.run(
                    f"MATCH (a:Entity {{id: $source_id}}) "
                    f"MATCH (b:Entity {{id: $target_id}}) "
                    f"MERGE (a)-[r:{rel_type}]->(b) SET r += $props "
                    f"RETURN count(r) as cnt",
                    source_id=source_id,
                    target_id=target_id,
                    props=props,
                )
                record = result.single()
                if record and record["cnt"] > 0:
                    created += 1
                else:
                    skipped += 1

            return created, skipped

        with self._session() as session:
            session.execute_write(_tx_func, rels)

        return created, skipped

    # ── Query operations ──────────────────────────────────────────────────

    def get_entity(self, entity_id: str) -> Entity | None:
        """Get a single entity by ID. Returns proper subclass instance."""
        with self._session() as session:
            result = session.run(
                "MATCH (n:Entity {id: $id}) RETURN n",
                id=entity_id,
            )
            record = result.single()
            if record is None:
                return None
            return self._record_to_entity(record["n"])

    def get_entities_by_type(self, entity_type: EntityType) -> list[Entity]:
        """Get all entities of a specific type."""
        label = entity_type.value
        with self._session() as session:
            result = session.run(f"MATCH (n:{label}) RETURN n")
            return [self._record_to_entity(record["n"]) for record in result]

    def count_nodes(self) -> dict[str, int]:
        """Count nodes per entity type label."""
        counts: dict[str, int] = {}
        with self._session() as session:
            for entity_type in EntityType:
                label = entity_type.value
                result = session.run(f"MATCH (n:{label}) RETURN count(n) as cnt")
                record = result.single()
                counts[label] = record["cnt"] if record else 0
        return counts

    def count_relationships(self) -> dict[str, int]:
        """Count relationships per type."""
        counts: dict[str, int] = {}
        with self._session() as session:
            result = session.run(
                "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as cnt"
            )
            for record in result:
                counts[record["rel_type"]] = record["cnt"]
        return counts

    def count_orphan_nodes(self) -> int:
        """Count nodes with zero relationships (should be 0 after loading)."""
        with self._session() as session:
            result = session.run(
                "MATCH (n:Entity) WHERE NOT (n)--() RETURN count(n) as cnt"
            )
            record = result.single()
            return record["cnt"] if record else 0

    def traverse(
        self,
        start_id: str,
        relationship_types: list[str] | None = None,
        max_hops: int = 3,
        target_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Multi-hop traversal from a starting node.

        Returns list of paths as dicts with 'nodes' and 'relationships'.
        """
        rel_filter = ""
        if relationship_types:
            rel_filter = ":" + "|".join(relationship_types)

        target_filter = ""
        if target_type:
            target_filter = f":{target_type}"

        query = (
            f"MATCH path = (start:Entity {{id: $start_id}})"
            f"-[{rel_filter}*1..{max_hops}]->"
            f"(end{target_filter}) "
            f"RETURN path LIMIT 100"
        )

        paths = []
        with self._session() as session:
            result = session.run(query, start_id=start_id)
            for record in result:
                path = record["path"]
                nodes = [self._node_to_dict(node) for node in path.nodes]
                rels = [
                    {
                        "type": rel.type,
                        "source": rel.start_node["id"],
                        "target": rel.end_node["id"],
                    }
                    for rel in path.relationships
                ]
                paths.append({"nodes": nodes, "relationships": rels})

        return paths

    # ── Entity resolution ─────────────────────────────────────────────

    def resolve_entities(
        self, terms: list[str], limit_per_term: int = 5
    ) -> dict[str, list[dict[str, Any]]]:
        """Resolve natural language terms to Neo4j node IDs.

        Uses three strategies in order:
        1. Exact ID match
        2. Pattern-based conversion (e.g., "Article 9" → "GDPR_ART_9")
        3. Fuzzy text search on id, name, title, term fields

        Returns {term: [matched_nodes]} mapping.
        """
        resolved: dict[str, list[dict[str, Any]]] = {}

        for term in terms:
            matches: list[dict[str, Any]] = []

            # Strategy 1: Exact ID match
            exact = self._find_node_by_id(term)
            if exact:
                matches.append(exact)
                resolved[term] = matches
                continue

            # Strategy 2: Pattern-based ID conversion
            candidate_ids = self._pattern_convert(term)
            for cid in candidate_ids:
                node = self._find_node_by_id(cid)
                if node and not any(m["id"] == node["id"] for m in matches):
                    matches.append(node)

            if matches:
                resolved[term] = matches[:limit_per_term]
                continue

            # Strategy 3: Fuzzy text search
            fuzzy = self._fuzzy_search(term, limit_per_term)
            resolved[term] = fuzzy

        return resolved

    def _find_node_by_id(self, node_id: str) -> dict[str, Any] | None:
        """Find a node by exact ID match."""
        with self._session() as session:
            result = session.run(
                "MATCH (n:Entity {id: $id}) RETURN n LIMIT 1",
                id=node_id,
            )
            record = result.single()
            if record:
                return self._node_to_dict(record["n"])
        return None

    def _pattern_convert(self, term: str) -> list[str]:
        """Convert common natural language patterns to Neo4j ID candidates."""
        candidates: list[str] = []
        t = term.strip()
        t_lower = t.lower()

        # "Article 9" / "Art. 9" / "Article 5(1)(c)" → GDPR_ART_9, AIACT_ART_9
        art_match = re.match(
            r"(?:article|art\.?)\s*(\d+)", t_lower
        )
        if art_match:
            num = art_match.group(1)
            candidates.extend([f"GDPR_ART_{num}", f"AIACT_ART_{num}"])

        # "Annex III" / "Annex 3" → AIACT_ANNEX_III
        annex_match = re.match(r"annex\s+(i+v?|vi*|[0-9]+)", t_lower)
        if annex_match:
            raw = annex_match.group(1).upper()
            candidates.append(f"AIACT_ANNEX_{raw}")

        # "Recital 71" → GDPR_REC_71, AIACT_REC_71
        rec_match = re.match(r"recital\s+(\d+)", t_lower)
        if rec_match:
            num = rec_match.group(1)
            candidates.extend([f"GDPR_REC_{num}", f"AIACT_REC_{num}"])

        # Try common prefixed forms
        normalized = re.sub(r"[^a-z0-9]+", "_", t_lower).strip("_").upper()
        candidates.extend([
            f"CONCEPT_{normalized}",
            f"AIST_{normalized}",
            f"RISK_{normalized}",
            f"GDPR_DEF_{normalized}",
        ])

        return candidates

    def _fuzzy_search(
        self, term: str, limit: int = 5
    ) -> list[dict[str, Any]]:
        """Fuzzy search for nodes matching a term via text containment."""
        # Split multi-word terms into search tokens
        tokens = [t for t in re.split(r"[_\s]+", term.lower()) if len(t) > 2]
        if not tokens:
            tokens = [term.lower()]

        # Build a WHERE clause that matches any token in id, name, or title
        conditions = []
        params: dict[str, Any] = {"limit": limit}
        for i, tok in enumerate(tokens[:3]):  # max 3 tokens
            key = f"tok{i}"
            params[key] = tok
            conditions.append(
                f"(toLower(n.id) CONTAINS ${key} "
                f"OR toLower(coalesce(n.name, '')) CONTAINS ${key} "
                f"OR toLower(coalesce(n.title, '')) CONTAINS ${key} "
                f"OR toLower(coalesce(n.term, '')) CONTAINS ${key})"
            )

        where_clause = " AND ".join(conditions)
        query = (
            f"MATCH (n:Entity) WHERE {where_clause} "
            f"RETURN n LIMIT $limit"
        )

        nodes: list[dict[str, Any]] = []
        with self._session() as session:
            result = session.run(query, **params)
            for record in result:
                nodes.append(self._node_to_dict(record["n"]))

        return nodes

    def get_node_neighborhood(
        self, node_id: str, max_rels: int = 20
    ) -> dict[str, Any]:
        """Get a node and its immediate neighbors for visualization."""
        with self._session() as session:
            result = session.run(
                "MATCH (n:Entity {id: $id}) "
                "OPTIONAL MATCH (n)-[r]-(m:Entity) "
                "RETURN n, collect(DISTINCT {rel_type: type(r), "
                "target_id: m.id, target_name: m.name, "
                "target_type: m.type, direction: CASE WHEN startNode(r) = n "
                "THEN 'outgoing' ELSE 'incoming' END})[0..$max_rels] AS neighbors",
                id=node_id,
                max_rels=max_rels,
            )
            record = result.single()
            if not record:
                return {}
            return {
                "node": self._node_to_dict(record["n"]),
                "neighbors": [dict(n) for n in record["neighbors"] if n.get("target_id")],
            }

    def clear_all(self) -> None:
        """Delete all nodes and relationships. USE WITH CAUTION."""
        with self._session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            logger.warning("All nodes and relationships deleted")

    # ── Internal helpers ──────────────────────────────────────────────────

    def _record_to_entity(self, node: Any) -> Entity:
        """Convert Neo4j node to proper Entity subclass.

        This fixes the core_2 bug where _record_to_entity() always returned
        base Entity class, losing all subclass fields.
        """
        import json

        props = dict(node)

        # Deserialize JSON-encoded complex fields
        for key in list(props.keys()):
            val = props[key]
            if isinstance(val, str) and val.startswith(("{", "[")):
                try:
                    props[key] = json.loads(val)
                except (json.JSONDecodeError, ValueError):
                    pass

        # Reconstruct provenance from prov_* fields
        provenance = {}
        for key in list(props.keys()):
            if key.startswith("prov_"):
                provenance[key[5:]] = props.pop(key)
        if provenance:
            props["provenance"] = provenance

        return entity_from_dict(props)

    @staticmethod
    def _node_to_dict(node: Any) -> dict[str, Any]:
        """Convert Neo4j node to simple dict."""
        return dict(node)
