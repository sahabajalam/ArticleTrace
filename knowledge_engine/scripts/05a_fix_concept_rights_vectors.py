"""Phase 5a: Fix empty concepts and rights vector store collections.

Targeted script that only embeds the 2 missing collections,
reusing logic from 05_load_vector_store.py.

Usage:
    uv run python scripts/05a_fix_concept_rights_vectors.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

PARSED_DATA_DIR = PROJECT_ROOT / "parsed_data"


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def get_embedding_client():
    """Initialize Gemini embedding client."""
    from src.config import settings
    from google import genai

    client = genai.Client(api_key=settings.google_api_key)
    return client


def embed_batch(client, texts: list[str], model: str = "gemini-embedding-001") -> list[list[float]]:
    """Embed a batch of texts with rate limiting."""
    from google.genai import types

    embeddings = []
    batch_size = 100

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        cleaned = []
        for t in batch:
            t = t.strip()
            if not t:
                t = "empty"
            if len(t) > 8000:
                t = t[:8000]
            cleaned.append(t)

        try:
            result = client.models.embed_content(
                model=model,
                contents=cleaned,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                ),
            )
            for emb in result.embeddings:
                embeddings.append(emb.values)
        except Exception as e:
            print(f"  Embedding error at batch {i}: {e}")
            time.sleep(5)
            try:
                result = client.models.embed_content(
                    model=model,
                    contents=cleaned,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT",
                    ),
                )
                for emb in result.embeddings:
                    embeddings.append(emb.values)
            except Exception as e2:
                print(f"  Retry failed: {e2}")
                embeddings.extend([[0.0] * 3072] * len(cleaned))

        if i + batch_size < len(texts):
            time.sleep(0.5)

    return embeddings


def prepare_concept_docs() -> tuple[list[str], list[str], list[dict]]:
    """Prepare concept documents for embedding."""
    ids, texts, metas = [], [], []
    for concept in load_json(PARSED_DATA_DIR / "entities" / "concepts.json"):
        doc_text = (
            f"{concept.get('name', '')}. {concept.get('description', '')}. "
            f"Category: {concept.get('category', '')}. "
            f"Keywords: {', '.join(concept.get('keywords', []))}"
        )
        ids.append(concept["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": concept["id"],
            "type": "Concept",
            "category": concept.get("category", ""),
            "regulation_id": concept.get("regulation_id", ""),
        })
    return ids, texts, metas


def prepare_right_docs() -> tuple[list[str], list[str], list[dict]]:
    """Prepare right documents for embedding."""
    ids, texts, metas = [], [], []
    for right in load_json(PARSED_DATA_DIR / "entities" / "rights.json"):
        doc_text = f"{right.get('name', '')}. {right.get('description', '')}"
        ids.append(right["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": right["id"],
            "type": "Right",
            "regulation_id": right.get("regulation_id", ""),
            "right_holder": right.get("right_holder", ""),
        })
    return ids, texts, metas


def main():
    from src.stores.weaviate_store import WeaviateVectorStore
    from src.config import settings

    print("=" * 60)
    print("PHASE 5a: Fix concepts & rights vector store collections")
    print("=" * 60)

    # Initialize
    print("\n[1/4] Initializing...")
    client = get_embedding_client()
    vs = WeaviateVectorStore(
        host=settings.weaviate_host,
        http_port=settings.weaviate_http_port,
        grpc_port=settings.weaviate_grpc_port,
    )
    print(f"  Gemini client ready")
    print(f"  Weaviate: {settings.weaviate_host}:{settings.weaviate_http_port}")

    # ── Concepts ──────────────────────────────────────────────────
    print("\n[2/4] Embedding concepts...")
    ids, texts, metas = prepare_concept_docs()
    if ids:
        embeddings = embed_batch(client, texts)
        loaded = vs.add_documents("concepts", ids, texts, embeddings, metas)
        print(f"  concepts: {loaded} documents loaded")
    else:
        print("  ERROR: No concept data found in parsed_data/entities/concepts.json!")
        return 1

    # ── Rights ────────────────────────────────────────────────────
    print("\n[3/4] Embedding rights...")
    ids, texts, metas = prepare_right_docs()
    if ids:
        embeddings = embed_batch(client, texts)
        loaded = vs.add_documents("rights", ids, texts, embeddings, metas)
        print(f"  rights: {loaded} documents loaded")
    else:
        print("  ERROR: No rights data found in parsed_data/entities/rights.json!")
        return 1

    # ── Validation ────────────────────────────────────────────────
    print("\n[4/4] Validation...")
    print("\n" + "=" * 60)

    concepts_count = vs.count("concepts")
    rights_count = vs.count("rights")

    checks = {
        "concepts >= 40": concepts_count >= 40,
        "rights >= 15": rights_count >= 15,
    }

    all_pass = True
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {check} (actual: {concepts_count if 'concepts' in check else rights_count})")

    # Print full collection summary
    print()
    print("  FULL VECTOR STORE STATUS:")
    total = 0
    for coll_name in WeaviateVectorStore.COLLECTIONS:
        count = vs.count(coll_name)
        total += count
        print(f"    {coll_name:20s}: {count:5d} documents")
    print(f"    {'TOTAL':20s}: {total:5d} documents")

    print("=" * 60)
    if all_pass:
        print("ALL CHECKS PASS -- Concepts & Rights collections fixed!")
    else:
        print("SOME CHECKS FAILED.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
