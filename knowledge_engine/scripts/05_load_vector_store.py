"""Phase 5: Generate embeddings and load into Weaviate vector store.

Uses Gemini text-embedding-004 for embeddings.
Requires a running Weaviate instance (see docker-compose.yml).

Collections:
  articles     - 212 articles (full_text)
  recitals     - 353 recitals (text)
  interpretive - 56 docs (guidelines + case law + enforcement)
  definitions  - 90 definitions (definition_text)
  obligations  - 1421 obligations + exemptions (source_text)
  concepts     - ~50 regulatory concepts (description + keywords)
  rights       - ~20 data subject rights (description)

Rate limiting: Gemini embedding API = 1500 RPM, batched at 100 docs/request.
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
    """Embed a batch of texts with rate limiting.

    Gemini embedding API accepts up to 100 texts per batch.
    """
    from google.genai import types

    embeddings = []
    batch_size = 100

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        # Clean texts: remove empty, truncate long ones
        cleaned = []
        for t in batch:
            t = t.strip()
            if not t:
                t = "empty"
            # Gemini text-embedding-004 has 2048 token limit, ~8000 chars safe
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
            # Rate limit backoff
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
                # Fallback: zero vectors
                embeddings.extend([[0.0] * 3072] * len(cleaned))

        # Small delay to respect rate limits
        if i + batch_size < len(texts):
            time.sleep(0.5)

    return embeddings


def prepare_article_docs(articles: list[dict]) -> tuple[list[str], list[str], list[dict]]:
    """Prepare article documents for embedding."""
    ids, texts, metas = [], [], []
    for art in articles:
        doc_text = f"{art.get('name', '')}. {art.get('full_text', '')}"
        ids.append(art["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": art["id"],
            "type": "Article",
            "regulation_id": art.get("regulation_id", ""),
            "article_number": art.get("article_number", 0),
            "modality": art.get("modality", ""),
            "chapter": art.get("chapter", ""),
        })
    return ids, texts, metas


def prepare_recital_docs(recitals: list[dict]) -> tuple[list[str], list[str], list[dict]]:
    """Prepare recital documents for embedding."""
    ids, texts, metas = [], [], []
    for rec in recitals:
        doc_text = f"Recital {rec.get('recital_number', '')}. {rec.get('text', rec.get('full_text', ''))}"
        ids.append(rec["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": rec["id"],
            "type": "Recital",
            "regulation_id": rec.get("regulation_id", ""),
            "recital_number": rec.get("recital_number", 0),
        })
    return ids, texts, metas


def prepare_interpretive_docs() -> tuple[list[str], list[str], list[dict]]:
    """Prepare guidelines, case law, enforcement for embedding."""
    ids, texts, metas = [], [], []

    # Guidelines
    for gl in load_json(PARSED_DATA_DIR / "interpretive" / "edpb_guidelines.json"):
        # Guidelines can be huge - take first 5000 chars for embedding
        gl_text = f"{gl.get('name', '')}. {gl.get('full_text', '')[:5000]}"
        ids.append(gl["id"])
        texts.append(gl_text)
        metas.append({
            "entity_id": gl["id"],
            "type": "Guideline",
            "reference": gl.get("reference", ""),
            "topics": ", ".join(gl.get("topics", [])),
        })

    # Case law
    for case in load_json(PARSED_DATA_DIR / "interpretive" / "case_law.json"):
        case_text = (
            f"{case.get('name', '')}. {case.get('topic', '')}. "
            f"{case.get('holding', '')}. {case.get('facts', '')}"
        )
        ids.append(case["id"])
        texts.append(case_text)
        metas.append({
            "entity_id": case["id"],
            "type": "CaseLaw",
            "case_number": case.get("case_number", ""),
            "court": case.get("court", ""),
            "topic": case.get("topic", ""),
        })

    # Enforcement
    for enf in load_json(PARSED_DATA_DIR / "interpretive" / "enforcement_actions.json"):
        enf_text = (
            f"{enf.get('name', '')}. {enf.get('description', '')}. "
            f"{enf.get('summary', enf.get('full_text', '')[:3000])}"
        )
        ids.append(enf["id"])
        texts.append(enf_text)
        metas.append({
            "entity_id": enf["id"],
            "type": "EnforcementAction",
            "authority": enf.get("authority", ""),
            "fine_amount": enf.get("fine_amount", ""),
        })

    return ids, texts, metas


def prepare_definition_docs(definitions: list[dict]) -> tuple[list[str], list[str], list[dict]]:
    """Prepare definition documents for embedding."""
    ids, texts, metas = [], [], []
    for defn in definitions:
        doc_text = f"{defn.get('term', '')} means {defn.get('definition_text', '')}"
        ids.append(defn["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": defn["id"],
            "type": "Definition",
            "term": defn.get("term", ""),
            "regulation_id": defn.get("regulation_id", ""),
        })
    return ids, texts, metas


def prepare_obligation_docs() -> tuple[list[str], list[str], list[dict]]:
    """Prepare obligation and exemption documents for embedding."""
    ids, texts, metas = [], [], []

    for obl in load_json(PARSED_DATA_DIR / "entities" / "obligations.json"):
        doc_text = f"{obl.get('name', '')}. {obl.get('source_text', '')}"
        ids.append(obl["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": obl["id"],
            "type": "Obligation",
            "obligation_type": obl.get("obligation_type", ""),
            "regulation_id": obl.get("regulation_id", ""),
            "article_reference": obl.get("article_reference", ""),
            "duty_bearer": obl.get("duty_bearer", ""),
        })

    for ex in load_json(PARSED_DATA_DIR / "entities" / "exemptions.json"):
        doc_text = f"{ex.get('name', '')}. {ex.get('source_text', '')}"
        ids.append(ex["id"])
        texts.append(doc_text)
        metas.append({
            "entity_id": ex["id"],
            "type": "Exemption",
            "obligation_type": ex.get("obligation_type", ""),
            "regulation_id": ex.get("regulation_id", ""),
            "article_reference": ex.get("article_reference", ""),
        })

    return ids, texts, metas


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


class _Neo4jVectorWriter:
    """Minimal write/count adapter that targets the Neo4j vector index.

    Mirrors the old WeaviateVectorStore interface this script relied on
    (add_documents, count, clear_all) so the rest of `main()` stays
    untouched. Embeddings are stored as :Entity.embedding properties;
    documents land in :Entity.document_text.
    """

    BATCH_SIZE = 250

    def __init__(self, graph_store):
        self.graph_store = graph_store

    def add_documents(self, collection, ids, documents, embeddings, metadatas):
        items = [
            {
                "id": ids[i],
                "embedding": embeddings[i],
                "collection": collection,
                "document": documents[i],
            }
            for i in range(len(ids))
        ]
        written = 0
        with self.graph_store._driver.session() as session:
            for start in range(0, len(items), self.BATCH_SIZE):
                chunk = items[start : start + self.BATCH_SIZE]
                record = session.run(
                    "UNWIND $items AS item "
                    "MATCH (n:Entity {id: item.id}) "
                    "SET n.embedding = item.embedding, "
                    "    n.collection = item.collection, "
                    "    n.document_text = item.document "
                    "RETURN count(n) AS updated",
                    items=chunk,
                ).single()
                written += record["updated"] if record else 0
        return written

    def count(self, collection):
        with self.graph_store._driver.session() as session:
            record = session.run(
                "MATCH (n:Entity) "
                "WHERE n.collection = $coll AND n.embedding IS NOT NULL "
                "RETURN count(n) AS cnt",
                coll=collection,
            ).single()
            return record["cnt"] if record else 0

    def clear_all(self):
        with self.graph_store._driver.session() as session:
            session.run(
                "MATCH (n:Entity) "
                "WHERE n.embedding IS NOT NULL "
                "REMOVE n.embedding, n.collection, n.document_text"
            )


def main():
    from src.stores.graph_store import GraphStore
    from src.config import settings

    print("=" * 60)
    print("PHASE 5: Load Vector Store (Neo4j vector index + Gemini Embeddings)")
    print("=" * 60)

    # Initialize
    print("\n[1/7] Initializing...")
    client = get_embedding_client()
    graph = GraphStore(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )
    vs = _Neo4jVectorWriter(graph)
    print(f"  Gemini client ready")
    print(f"  Neo4j: {settings.neo4j_uri}")

    # Clear if requested
    if "--clear" in sys.argv:
        print("  Clearing existing collections...")
        vs.clear_all()

    # ── Articles ──────────────────────────────────────────────────
    print("\n[2/7] Embedding articles...")
    gdpr_arts = load_json(PARSED_DATA_DIR / "legal" / "gdpr_articles.json")
    ai_arts = load_json(PARSED_DATA_DIR / "legal" / "eu_ai_act_articles.json")
    ids, texts, metas = prepare_article_docs(gdpr_arts + ai_arts)
    embeddings = embed_batch(client, texts)
    loaded = vs.add_documents("articles", ids, texts, embeddings, metas)
    print(f"  articles: {loaded} documents loaded")

    # ── Recitals ──────────────────────────────────────────────────
    print("\n[3/7] Embedding recitals...")
    gdpr_recs = load_json(PARSED_DATA_DIR / "legal" / "gdpr_recitals.json")
    ai_recs = load_json(PARSED_DATA_DIR / "legal" / "ai_act_recitals.json")
    ids, texts, metas = prepare_recital_docs(gdpr_recs + ai_recs)
    embeddings = embed_batch(client, texts)
    loaded = vs.add_documents("recitals", ids, texts, embeddings, metas)
    print(f"  recitals: {loaded} documents loaded")

    # ── Interpretive ──────────────────────────────────────────────
    print("\n[4/7] Embedding interpretive documents...")
    ids, texts, metas = prepare_interpretive_docs()
    embeddings = embed_batch(client, texts)
    loaded = vs.add_documents("interpretive", ids, texts, embeddings, metas)
    print(f"  interpretive: {loaded} documents loaded")

    # ── Definitions ───────────────────────────────────────────────
    print("\n[5/7] Embedding definitions...")
    defs = load_json(PARSED_DATA_DIR / "entities" / "definitions.json")
    ids, texts, metas = prepare_definition_docs(defs)
    embeddings = embed_batch(client, texts)
    loaded = vs.add_documents("definitions", ids, texts, embeddings, metas)
    print(f"  definitions: {loaded} documents loaded")

    # ── Obligations ───────────────────────────────────────────────
    print("\n[6/9] Embedding obligations + exemptions...")
    ids, texts, metas = prepare_obligation_docs()
    embeddings = embed_batch(client, texts)
    loaded = vs.add_documents("obligations", ids, texts, embeddings, metas)
    print(f"  obligations: {loaded} documents loaded")

    # ── Concepts ──────────────────────────────────────────────────
    print("\n[7/9] Embedding concepts...")
    ids, texts, metas = prepare_concept_docs()
    if ids:
        embeddings = embed_batch(client, texts)
        loaded = vs.add_documents("concepts", ids, texts, embeddings, metas)
        print(f"  concepts: {loaded} documents loaded")
    else:
        print("  concepts: 0 (no data)")

    # ── Rights ────────────────────────────────────────────────────
    print("\n[8/9] Embedding rights...")
    ids, texts, metas = prepare_right_docs()
    if ids:
        embeddings = embed_batch(client, texts)
        loaded = vs.add_documents("rights", ids, texts, embeddings, metas)
        print(f"  rights: {loaded} documents loaded")
    else:
        print("  rights: 0 (no data)")

    # ── Summary ───────────────────────────────────────────────────
    print("\n[9/9] Validation...")
    print("\n" + "=" * 60)
    print("VECTOR STORE SUMMARY")
    print("=" * 60)

    total = 0
    for coll_name in GraphStore.VECTOR_COLLECTIONS:
        count = vs.count(coll_name)
        total += count
        print(f"  {coll_name:20s}: {count:5d} documents")
    print(f"  {'TOTAL':20s}: {total:5d} documents")

    # Ensure the vector index exists (idempotent)
    graph.create_vector_index()
    print(f"  Vector index '{GraphStore.VECTOR_INDEX_NAME}' ensured.")

    # Exit gate
    checks = {
        "articles >= 200": vs.count("articles") >= 200,
        "recitals >= 300": vs.count("recitals") >= 300,
        "interpretive >= 40": vs.count("interpretive") >= 40,
        "definitions >= 80": vs.count("definitions") >= 80,
        "obligations >= 1000": vs.count("obligations") >= 1000,
        "concepts >= 40": vs.count("concepts") >= 40,
        "rights >= 15": vs.count("rights") >= 15,
    }

    print()
    all_pass = True
    for check, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_pass = False
        print(f"  [{status}] {check}")

    print("=" * 60)
    if all_pass:
        print("ALL CHECKS PASS -- Vector store loaded successfully.")
    else:
        print("SOME CHECKS FAILED.")

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
