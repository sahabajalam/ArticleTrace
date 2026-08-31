"""Restore a JSONL backup (from scripts/10_backup_to_jsonl.py) into Neo4j.

Reads from backups/<TS>_nodes.jsonl + <TS>_rels.jsonl + <TS>_indexes.json.
Writes into the instance pointed at by .env (NEO4J_URI / USER / PASSWORD).

Mapping strategy: every node has an `id` property under a `:Entity(id)`
unique constraint. We build an in-memory map `old_element_id -> id` while
creating nodes, then look up by `id` when creating relationships. Element
IDs are not portable across instances; properties are.

SAFETY:
- This script CREATEs everything. Run it ONLY against an empty target
  instance, or the script will fail on the `:Entity(id)` unique constraint
  the moment a duplicate `id` is inserted. The empty-target check at startup
  is a guard, not a hard stop — pass --force to bypass for partial restores.

Usage (macOS / Linux; `uv sync` first if .venv does not exist yet):
  cd knowledge_engine
  ./.venv/bin/python scripts/11_restore_from_jsonl.py <TS>
  # e.g.
  ./.venv/bin/python scripts/11_restore_from_jsonl.py 20260619_183622

  On Windows the interpreter is ./.venv/Scripts/python.exe instead.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    if not args:
        print("Usage: 11_restore_from_jsonl.py <TIMESTAMP> [--force]")
        print("       (e.g. 11_restore_from_jsonl.py 20260619_183622)")
        return 2

    ts = args[0]
    backup_dir = PROJECT_ROOT / "backups"
    nodes_path = backup_dir / f"{ts}_nodes.jsonl"
    rels_path = backup_dir / f"{ts}_rels.jsonl"
    indexes_path = backup_dir / f"{ts}_indexes.json"
    meta_path = backup_dir / f"{ts}_meta.json"

    for p in (nodes_path, rels_path, indexes_path, meta_path):
        if not p.exists():
            print(f"[ERR] Missing backup file: {p}")
            return 1

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    print(f"Target URI: {settings.neo4j_uri}")
    print(f"Source URI (from meta): {meta.get('source_uri')}")
    print(f"Backup timestamp: {meta.get('timestamp_utc')}")
    print(f"Expected: {meta['node_count']} nodes, {meta['rel_count']} rels")
    print()

    if settings.neo4j_uri == meta.get("source_uri"):
        print("[!] Target URI matches the backup's source URI.")
        print("    This means you'd restore the data back onto itself.")
        if not force:
            print("    Pass --force to override. Aborting.")
            return 1

    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    try:
        with driver.session() as session:
            existing = list(session.run("MATCH (n) RETURN count(n) AS c"))[0]["c"]
            if existing and not force:
                print(f"[ERR] Target instance is not empty ({existing} nodes). "
                      f"Pass --force to override, or drop with MATCH (n) DETACH DELETE n.")
                return 1
            print(f"[OK] Target instance has {existing} nodes (proceeding)")
            print()

            # ---- 1. Recreate constraint(s) first so node creation enforces uniqueness ----
            print("[1/4] Recreating :Entity(id) unique constraint ...")
            session.run(
                "CREATE CONSTRAINT entity_id_unique IF NOT EXISTS "
                "FOR (n:Entity) REQUIRE n.id IS UNIQUE"
            )
            print("  [OK]")
            print()

            # ---- 2. Load nodes; build old_eid -> id map ----
            print(f"[2/4] Loading {meta['node_count']} nodes from {nodes_path.name} ...")
            eid_to_id: dict[str, str] = {}
            batch: list[dict] = []
            BATCH_SIZE = 100

            def flush_node_batch(batch: list[dict]) -> int:
                if not batch:
                    return 0
                # UNWIND lets us bulk-create while preserving per-node labels via APOC...
                # but Aura Free doesn't have APOC. So use a per-label-set CALL with dynamic labels via parameter.
                # Simpler: since every node is :Entity + one specialised label, group by the specialised one.
                # Here we just CREATE each with its full label set inlined via parameters.
                for node in batch:
                    labels = ":".join(node["labels"])
                    session.run(
                        f"CREATE (n:{labels}) SET n = $props",
                        props=node["properties"],
                    )
                return len(batch)

            count = 0
            with nodes_path.open("r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    batch.append(rec)
                    eid_to_id[rec["eid"]] = rec["properties"].get("id")
                    if len(batch) >= BATCH_SIZE:
                        count += flush_node_batch(batch)
                        batch = []
                        if count % 500 == 0:
                            print(f"  ... {count} nodes")
            count += flush_node_batch(batch)
            print(f"  [OK] {count} nodes loaded")
            print()

            # ---- 3. Load relationships by id-lookup ----
            print(f"[3/4] Loading {meta['rel_count']} relationships from {rels_path.name} ...")
            count = 0
            skipped = 0
            with rels_path.open("r", encoding="utf-8") as f:
                for line in f:
                    rec = json.loads(line)
                    start_id = eid_to_id.get(rec["start"])
                    end_id = eid_to_id.get(rec["end"])
                    if not start_id or not end_id:
                        skipped += 1
                        continue
                    session.run(
                        f"MATCH (a:Entity {{id: $s}}), (b:Entity {{id: $e}}) "
                        f"CREATE (a)-[r:{rec['type']}]->(b) SET r = $props",
                        s=start_id, e=end_id, props=rec.get("properties") or {},
                    )
                    count += 1
                    if count % 500 == 0:
                        print(f"  ... {count} rels")
            print(f"  [OK] {count} rels loaded ({skipped} skipped due to missing endpoint id)")
            print()

            # ---- 4. Recreate indexes ----
            print(f"[4/4] Recreating indexes from {indexes_path.name} ...")
            indexes_meta = json.loads(indexes_path.read_text(encoding="utf-8"))
            for vidx in indexes_meta["vector_indexes"]:
                name = vidx["name"]
                labels = vidx.get("labelsOrTypes") or ["Entity"]
                props = vidx.get("properties") or ["embedding"]
                # Vector indexes need dimensions + similarity. Pull from the
                # known-correct values; see SYSTEM.md §2.1.
                dims = 3072
                similarity = "cosine"
                session.run(
                    f"CREATE VECTOR INDEX {name} IF NOT EXISTS "
                    f"FOR (n:{labels[0]}) ON (n.{props[0]}) "
                    f"OPTIONS {{ indexConfig: {{ "
                    f"`vector.dimensions`: {dims}, "
                    f"`vector.similarity_function`: '{similarity}' "
                    f"}} }}"
                )
                print(f"  [OK] vector index '{name}' ({labels[0]}.{props[0]}, dim={dims})")
            print()

            # ---- Verification ----
            print("Verification:")
            n = list(session.run("MATCH (n) RETURN count(n) AS c"))[0]["c"]
            r = list(session.run("MATCH ()-[r]->() RETURN count(r) AS c"))[0]["c"]
            e = list(session.run(
                "MATCH (n) WHERE n.embedding IS NOT NULL RETURN count(n) AS c"
            ))[0]["c"]
            print(f"  Nodes:      {n:,} / {meta['node_count']:,}")
            print(f"  Rels:       {r:,} / {meta['rel_count']:,}")
            print(f"  Embeddings: {e:,}")
            ok = (n == meta["node_count"] and r == meta["rel_count"])
            print(f"  Status:     {'OK' if ok else 'MISMATCH'}")
            return 0 if ok else 1
    finally:
        driver.close()


if __name__ == "__main__":
    sys.exit(main())
