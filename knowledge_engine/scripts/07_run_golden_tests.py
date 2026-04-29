"""Run golden query test suite against the reasoning engine.

Loads test cases from golden_tests/test_queries.json, runs each through
the reasoning engine, and validates against expected outputs.

Usage:
    python scripts/07_run_golden_tests.py           # All tests
    python scripts/07_run_golden_tests.py --dry-run  # Retrieval only, no LLM
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GOLDEN_TESTS_PATH = PROJECT_ROOT / "golden_tests" / "test_queries.json"


def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 60)
    print("GOLDEN QUERY TEST SUITE")
    print("=" * 60)

    # Load test cases
    test_cases = json.loads(GOLDEN_TESTS_PATH.read_text(encoding="utf-8"))
    print(f"\nLoaded {len(test_cases)} test cases")

    # Initialize engine — Neo4j hosts both the graph and the vector index.
    from google import genai
    from src.config import settings
    from src.stores.graph_store import GraphStore
    from src.retrieval.engine import RetrievalEngine

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
        default_top_k=15,
        max_hops=2,
    )

    reasoner = None
    if not dry_run:
        from src.retrieval.reasoning_engine import ReasoningEngine
        reasoner = ReasoningEngine(
            retrieval_engine=engine,
            genai_client=genai_client,
            model="gemini-2.0-flash",
        )

    # Run tests
    results: list[dict] = []
    passed = 0
    failed = 0

    for tc in test_cases:
        print(f"\n--- {tc['id']}: {tc['description']} ---")
        print(f"  Query: {tc['query'][:80]}...")

        # Retrieval check
        retrieval_results = engine.query(tc["query"], top_k=15)
        retrieved_ids = {r["entity_id"] for r in retrieval_results}

        # Check expected citations appear in retrieval
        citation_hits = [c for c in tc["expected_citations"] if c in retrieved_ids]
        citation_miss = [c for c in tc["expected_citations"] if c not in retrieved_ids]

        # Check expected entities appear in retrieval
        entity_hits = [e for e in tc["expected_entities"] if e in retrieved_ids]
        entity_miss = [e for e in tc["expected_entities"] if e not in retrieved_ids]

        # Reasoning check (if not dry-run)
        answer_type_match = None
        if reasoner:
            from src.retrieval.query_models import ComplianceQueryRequest
            request = ComplianceQueryRequest(
                question=tc["query"], max_results=15, include_reasoning=False,
            )
            response = reasoner.answer(request)
            answer_type_match = response.answer_type == tc["expected_answer_type"]
            print(f"  Answer type: {response.answer_type} (expected: {tc['expected_answer_type']}) {'MATCH' if answer_type_match else 'MISMATCH'}")
            print(f"  Confidence: {response.confidence.value}")

        # Score
        total_expected = len(tc["expected_citations"]) + len(tc["expected_entities"])
        total_found = len(citation_hits) + len(entity_hits)
        retrieval_score = total_found / max(total_expected, 1)

        test_pass = retrieval_score >= 0.5  # At least half of expected entities found
        if answer_type_match is not None:
            test_pass = test_pass and answer_type_match

        status = "PASS" if test_pass else "FAIL"
        if test_pass:
            passed += 1
        else:
            failed += 1

        print(f"  Citations: {len(citation_hits)}/{len(tc['expected_citations'])} found {citation_miss if citation_miss else ''}")
        print(f"  Entities:  {len(entity_hits)}/{len(tc['expected_entities'])} found {entity_miss if entity_miss else ''}")
        print(f"  Retrieval score: {retrieval_score:.0%}")
        print(f"  [{status}]")

        results.append({
            "id": tc["id"],
            "status": status,
            "retrieval_score": retrieval_score,
            "citation_hits": citation_hits,
            "citation_miss": citation_miss,
            "entity_hits": entity_hits,
            "entity_miss": entity_miss,
            "answer_type_match": answer_type_match,
        })

    # Summary
    print("\n" + "=" * 60)
    print("GOLDEN TEST RESULTS")
    print("=" * 60)
    for r in results:
        print(f"  [{r['status']}] {r['id']} (retrieval: {r['retrieval_score']:.0%})")
    print(f"\n  Passed: {passed}/{len(test_cases)}")
    print(f"  Failed: {failed}/{len(test_cases)}")
    print(f"  Pass rate: {100 * passed / max(len(test_cases), 1):.0f}%")
    print("=" * 60)

    graph.close()
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
