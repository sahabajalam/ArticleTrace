"""Stream-dump the live Neo4j instance to JSONL.

Reads from the instance pointed at by .env (NEO4J_URI / USER / PASSWORD).
Writes:
  backups/<TS>_nodes.jsonl    — one node per line {labels, properties}
  backups/<TS>_rels.jsonl     — one rel per line  {type, start, end, properties}
  backups/<TS>_indexes.json   — vector + property indexes
  backups/<TS>_meta.json      — counts + source URI + timestamp

Streaming + line-delimited so a mid-export drop is recoverable rather than corrupt.
Embeddings (lists of 3072 floats) are preserved as JSON arrays.

Usage:
  cd knowledge_engine
  ./.venv/Scripts/python.exe scripts/10_backup_to_jsonl.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402


def main() -> int:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = PROJECT_ROOT / "backups"
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes_path = out_dir / f"{ts}_nodes.jsonl"
    rels_path = out_dir / f"{ts}_rels.jsonl"
    indexes_path = out_dir / f"{ts}_indexes.json"
    meta_path = out_dir / f"{ts}_meta.json"

    print(f"Source URI: {settings.neo4j_uri}")
    print(f"Output dir: {out_dir}")
    print()

    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    node_count = 0
    rel_count = 0

    try:
        with driver.session() as session:
            print("[1/3] Dumping nodes -> ", nodes_path.name, " ...")
            with nodes_path.open("w", encoding="utf-8") as f:
                result = session.run("MATCH (n) RETURN n, elementId(n) AS eid, labels(n) AS labels")
                for record in result:
                    n = record["n"]
                    f.write(json.dumps({
                        "eid": record["eid"],
                        "labels": record["labels"],
                        "properties": dict(n),
                    }, default=str, ensure_ascii=False) + "\n")
                    node_count += 1
                    if node_count % 200 == 0:
                        print(f"  ... {node_count} nodes")
            print(f"  [OK] {node_count} nodes written")
            print()

            print("[2/3] Dumping relationships -> ", rels_path.name, " ...")
            with rels_path.open("w", encoding="utf-8") as f:
                result = session.run(
                    "MATCH (a)-[r]->(b) RETURN type(r) AS t, elementId(a) AS s, "
                    "elementId(b) AS e, properties(r) AS p"
                )
                for record in result:
                    f.write(json.dumps({
                        "type": record["t"],
                        "start": record["s"],
                        "end": record["e"],
                        "properties": dict(record["p"]),
                    }, default=str, ensure_ascii=False) + "\n")
                    rel_count += 1
                    if rel_count % 500 == 0:
                        print(f"  ... {rel_count} rels")
            print(f"  [OK] {rel_count} rels written")
            print()

            print("[3/3] Dumping indexes/constraints -> ", indexes_path.name, " ...")
            vector_indexes = [dict(r) for r in session.run("SHOW VECTOR INDEXES")]
            other_indexes = [dict(r) for r in session.run("SHOW INDEXES")]
            constraints = [dict(r) for r in session.run("SHOW CONSTRAINTS")]
            indexes_path.write_text(
                json.dumps({
                    "vector_indexes": vector_indexes,
                    "all_indexes": other_indexes,
                    "constraints": constraints,
                }, default=str, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"  [OK] {len(vector_indexes)} vector indexes, "
                  f"{len(other_indexes)} total indexes, {len(constraints)} constraints")
            print()
    finally:
        driver.close()

    meta = {
        "timestamp_utc": ts,
        "source_uri": settings.neo4j_uri,
        "source_user": settings.neo4j_user,
        "node_count": node_count,
        "rel_count": rel_count,
        "nodes_file": nodes_path.name,
        "rels_file": rels_path.name,
        "indexes_file": indexes_path.name,
    }
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print("=" * 60)
    print("BACKUP COMPLETE")
    print("=" * 60)
    print(f"  Timestamp: {ts}")
    print(f"  Nodes:     {node_count:,}")
    print(f"  Rels:      {rel_count:,}")
    print(f"  Output:    {out_dir}")
    print(f"  Sizes:")
    for p in (nodes_path, rels_path, indexes_path, meta_path):
        size_mb = p.stat().st_size / 1024 / 1024
        print(f"    {p.name:40s} {size_mb:8.2f} MB")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
