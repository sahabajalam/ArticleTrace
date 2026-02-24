"""Neo4j graph store for the EU AI Regulatory Knowledge Graph.

Fixes the core_2 _record_to_entity() roundtrip bug by using entity_from_dict()
to return proper subclass instances. Adds batch operations for loading 2000+ nodes.
"""

from __future__ import annotations

import logging
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
