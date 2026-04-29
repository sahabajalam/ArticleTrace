"""Demo: Run sample compliance queries against the knowledge base.

Tests the full Graph RAG pipeline:
  Query -> Embed -> Vector Search + Graph Traversal -> RRF Fusion -> Results

Usage:
  python scripts/06_demo_query.py            # Default query, retrieval only
  python scripts/06_demo_query.py 2          # Query index 2
  python scripts/06_demo_query.py --reason   # Full reasoning mode with LLM synthesis
  python scripts/06_demo_query.py --reason "Your custom question here"
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


DEMO_QUERIES = [
    "What are the requirements for automated decision-making under GDPR and AI Act?",
    "What penalties apply if a company deploys a prohibited AI system while processing personal data?",
    "What obligations does a provider of high-risk AI systems have regarding data governance?",
    "How do GDPR consent requirements interact with AI Act transparency obligations?",
    "What is the right to explanation for AI-driven decisions?",
]


def run_retrieval_demo(engine, query: str) -> None:
    """Run retrieval-only demo (original behavior)."""
    print(f"Query: {query}")
    print("-" * 60)

    results = engine.query(query, top_k=10)

    print(f"\nTop {len(results)} results (RRF-fused):\n")

    for i, r in enumerate(results):
        eid = r["entity_id"]
        rrf = r["rrf_score"]
        sources = "+".join(r["sources"])
        in_both = " [BOTH]" if r.get("in_both") else ""

        meta = r.get("metadata", {})
        etype = meta.get("type", "?")

        vsim = r.get("vector_similarity", 0)
        gscore = r.get("graph_score", 0)
        vrank = r.get("vector_rank", "-")
        grank = r.get("graph_rank", "-")

        print(f"  {i+1:2d}. [{etype:20s}] {eid}")
        print(f"      RRF: {rrf:.4f} | V-sim: {vsim:.3f} (rank {vrank}) | G-score: {gscore:.3f} (rank {grank}) | {sources}{in_both}")

        doc = r.get("document", "")
        if doc:
            snippet = doc[:150].replace("\n", " ")
            print(f"      {snippet}...")
        print()

    both_count = sum(1 for r in results if r.get("in_both"))
    vector_only = sum(1 for r in results if r["sources"] == ["vector"])
    graph_only = sum(1 for r in results if r["sources"] == ["graph"])
    print("-" * 60)
    print(f"Results in both: {both_count}, Vector-only: {vector_only}, Graph-only: {graph_only}")


def run_reasoning_demo(engine, genai_client, query: str) -> None:
    """Run full reasoning demo with LLM synthesis."""
    from src.retrieval.reasoning_engine import ReasoningEngine
    from src.retrieval.query_models import ComplianceQueryRequest

    print(f"Query: {query}")
    print("-" * 60)
    print("\n[Reasoning mode: retrieving + synthesizing...]\n")

    reasoner = ReasoningEngine(
        retrieval_engine=engine,
        genai_client=genai_client,
        model="gemini-2.0-flash",
    )

    request = ComplianceQueryRequest(
        question=query,
        max_results=10,
        include_reasoning=True,
    )

    response = reasoner.answer(request)

    # Print reasoning chain
    print("REASONING CHAIN:")
    for step in response.reasoning_chain:
        print(f"  Step {step.step_number}: [{step.action}] {step.description}")
        if step.entity_ids:
            print(f"    Entities: {', '.join(step.entity_ids[:5])}")
    print()

    # Print answer
    print("=" * 60)
    print(f"ANSWER TYPE: {response.answer_type}")
    print(f"CONFIDENCE:  {response.confidence.value}")
    print("=" * 60)
    print()
    print(response.answer)
    print()

    # Print citations
    if response.citations:
        print("-" * 60)
        print("CITATIONS:")
        for c in response.citations:
            verified = "verified" if c.relevance_score >= 0.8 else "unverified"
            print(f"  - {c.entity_id} ({c.regulation_id}) [{verified}]")
            if c.description:
                print(f"    {c.description}")

    print(f"\nRetrieval count: {response.retrieval_count}")


def main():
    from google import genai
    from src.config import settings
    from src.stores.graph_store import GraphStore
    from src.retrieval.engine import RetrievalEngine

    # Parse args
    args = sys.argv[1:]
    reason_mode = "--reason" in args
    args = [a for a in args if a != "--reason"]

    print("=" * 60)
    mode_label = "Reasoning" if reason_mode else "Retrieval"
    print(f"DEMO: Graph RAG Compliance Query Engine ({mode_label} Mode)")
    print("=" * 60)

    # Initialize stores — Neo4j hosts both the graph and the vector index.
    print("\nInitializing...")
    genai_client = genai.Client(api_key=settings.google_api_key)

    graph = GraphStore(
        uri=settings.neo4j_uri,
        user=settings.neo4j_user,
        password=settings.neo4j_password,
    )

    engine = RetrievalEngine(
        graph_store=graph,
        genai_client=genai_client,
        rrf_k=60,
        default_top_k=10,
        max_hops=2,
    )

    print("  Ready.\n")

    # Determine query
    query_idx = 0
    if args:
        try:
            query_idx = int(args[0])
        except ValueError:
            DEMO_QUERIES.insert(0, " ".join(args))
            query_idx = 0

    query = DEMO_QUERIES[min(query_idx, len(DEMO_QUERIES) - 1)]

    if reason_mode:
        run_reasoning_demo(engine, genai_client, query)
    else:
        run_retrieval_demo(engine, query)

    graph.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
