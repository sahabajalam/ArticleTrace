"""Phase 8: Migrate existing JSON-backed embeddings into Weaviate.

Reads the 7 collection JSON files in `chroma_data/` (legacy folder name)
and bulk-inserts every document into Weaviate WITHOUT re-embedding.
This preserves the ~2,198 embeddings already computed against Gemini.

Usage:
    python scripts/08_migrate_json_to_weaviate.py             # incremental
    python scripts/08_migrate_json_to_weaviate.py --clear     # drop & reload
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

JSON_DIR = PROJECT_ROOT / "chroma_data"


def main() -> int:
    from src.stores.weaviate_store import WeaviateVectorStore
    from src.config import settings

    print("=" * 60)
    print("PHASE 8: JSON -> Weaviate migration (reuses embeddings)")
    print("=" * 60)

    vs = WeaviateVectorStore(
        host=settings.weaviate_host,
        http_port=settings.weaviate_http_port,
        grpc_port=settings.weaviate_grpc_port,
    )

    if "--clear" in sys.argv:
        print("Clearing existing Weaviate collections...")
        vs.clear_all()

    total_added = 0
    for coll in WeaviateVectorStore.COLLECTIONS:
        src = JSON_DIR / f"{coll}.json"
        if not src.exists():
            print(f"  {coll:14s}: skipped (no JSON file)")
            continue

        data = json.loads(src.read_text(encoding="utf-8"))
        ids = data.get("ids", [])
        docs = data.get("documents", [])
        embs = data.get("embeddings", [])
        metas = data.get("metadatas", [])

        if not ids:
            print(f"  {coll:14s}: skipped (empty)")
            continue

        added = vs.add_documents(coll, ids, docs, embs, metas)
        total_added += added
        print(f"  {coll:14s}: {added} documents migrated (Weaviate total: {vs.count(coll)})")

    print("=" * 60)
    print(f"Total documents migrated this run: {total_added}")
    print("Migration complete.")
    vs.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
