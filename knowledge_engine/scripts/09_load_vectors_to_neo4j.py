"""Phase 9: Load embeddings from chroma_data/*.json into Neo4j.

Replaces the prior JSON / Weaviate vector backends with Neo4j's native
vector index. For each collection JSON file:
  1. UNWIND batch-update :Entity nodes by id, setting `embedding` and
     `collection` properties.
  2. Optionally also store `document` text on the node so retrieval can
     return text without a second lookup.

After all collections are loaded, creates the `entity_embedding` vector
index over :Entity(embedding) — single index, all 7 collections share it.

Idempotent: re-running just re-sets properties and re-MERGEs the index.

Usage:
    python scripts/09_load_vectors_to_neo4j.py
    python scripts/09_load_vectors_to_neo4j.py --skip-document  (don't store text)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

JSON_DIR = PROJECT_ROOT / "chroma_data"
BATCH_SIZE = 250


def main() -> int:
    from src.config import settings
    from src.stores.graph_store import GraphStore

    skip_document = "--skip-document" in sys.argv

    print("=" * 60)
    print("PHASE 9: load JSON embeddings into Neo4j vector index")
    print("=" * 60)
    print(f"  Source: {JSON_DIR}")
    print(f"  Target: {settings.neo4j_uri}")
    print()

    gs = GraphStore(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )

    total_updated = 0
    missing_total = 0

    try:
        with gs._driver.session() as session:
            for coll in GraphStore.VECTOR_COLLECTIONS:
                src = JSON_DIR / f"{coll}.json"
                if not src.exists():
                    print(f"  {coll:14s}: skipped (no JSON file)")
                    continue

                data = json.loads(src.read_text(encoding="utf-8"))
                ids = data.get("ids", [])
                docs = data.get("documents", [])
                embs = data.get("embeddings", [])

                if not ids:
                    print(f"  {coll:14s}: skipped (empty)")
                    continue

                items = []
                for i, eid in enumerate(ids):
                    item = {"id": eid, "embedding": embs[i], "collection": coll}
                    if not skip_document and i < len(docs):
                        item["document"] = docs[i]
                    items.append(item)

                updated = 0
                missing = 0
                for start in range(0, len(items), BATCH_SIZE):
                    chunk = items[start : start + BATCH_SIZE]
                    if skip_document:
                        cypher = (
                            "UNWIND $items AS item "
                            "MATCH (n:Entity {id: item.id}) "
                            "SET n.embedding = item.embedding, "
                            "    n.collection = item.collection "
                            "RETURN count(n) AS updated"
                        )
                    else:
                        cypher = (
                            "UNWIND $items AS item "
                            "MATCH (n:Entity {id: item.id}) "
                            "SET n.embedding = item.embedding, "
                            "    n.collection = item.collection, "
                            "    n.document_text = item.document "
                            "RETURN count(n) AS updated"
                        )
                    record = session.run(cypher, items=chunk).single()
                    upd = record["updated"] if record else 0
                    updated += upd
                    missing += len(chunk) - upd

                total_updated += updated
                missing_total += missing
                gap = f" ({missing} missing in graph)" if missing else ""
                print(f"  {coll:14s}: {updated} embeddings written{gap}")

        print()
        print(f"Creating vector index '{GraphStore.VECTOR_INDEX_NAME}' "
              f"(dim={GraphStore.VECTOR_DIMENSIONS}, cosine)...")
        gs.create_vector_index()

        print()
        print("=" * 60)
        print(f"Total: {total_updated} embeddings loaded "
              f"({missing_total} ids not found in graph)")
        print("Index creation requested — Neo4j will populate it asynchronously.")
        print("Check readiness via /health (vector_index: online).")
        print("=" * 60)
    finally:
        gs.close()

    return 0 if missing_total == 0 else 0  # non-fatal if some ids missing


if __name__ == "__main__":
    sys.exit(main())
