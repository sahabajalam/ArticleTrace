"""3-mode retrieval comparison on the expanded golden set.

For each query in golden_tests/test_queries.json, runs three retrieval modes
against the same expected_citations + expected_entities labels:

  - vector_only   : pure embedding search, no graph expansion
  - graph_only    : vector-seeded graph traversal (top-5 seeds, max 2 hops),
                    graph hits only — no vector hits in the result list
  - hybrid_rrf    : the production path (vector + graph + RRF fusion)

Outputs:
  - Per-query 3-column breakdown
  - Aggregate citation_recall + entity_recall + pass_rate per mode
  - Category breakdown (single_hop / multi_hop / out_of_scope) per mode
  - Writes a JSON artifact for METRICS.md to cite

Usage (macOS / Linux; `uv sync` first if .venv does not exist yet):
  cd knowledge_engine
  ./.venv/bin/python scripts/12_eval_three_mode.py

  On Windows the interpreter is ./.venv/Scripts/python.exe instead.
"""

from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GOLDEN_PATH = PROJECT_ROOT / "golden_tests" / "test_queries.json"
OUT_DIR = PROJECT_ROOT / "golden_tests"

TOP_K = 15
SEED_COUNT = 5
MAX_HOPS = 2


def score_mode(retrieved_ids: set[str], expected_citations: list[str], expected_entities: list[str]) -> dict:
    """Compute recall for citations and entities; return per-test record."""
    citation_hits = [c for c in expected_citations if c in retrieved_ids]
    entity_hits = [e for e in expected_entities if e in retrieved_ids]
    citation_miss = [c for c in expected_citations if c not in retrieved_ids]
    entity_miss = [e for e in expected_entities if e not in retrieved_ids]

    total_expected = len(expected_citations) + len(expected_entities)
    found = len(citation_hits) + len(entity_hits)
    score = found / max(total_expected, 1)

    return {
        "citation_hits": citation_hits,
        "citation_miss": citation_miss,
        "entity_hits": entity_hits,
        "entity_miss": entity_miss,
        "score": score,
        "pass": score >= 0.5,
    }


def main() -> int:
    from google import genai
    from src.config import settings
    from src.stores.graph_store import GraphStore
    from src.retrieval.engine import RetrievalEngine

    print("=" * 70)
    print("3-MODE RETRIEVAL COMPARISON")
    print("=" * 70)

    test_cases = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(test_cases)} test cases from {GOLDEN_PATH.name}")
    print(f"Top-k = {TOP_K}, seed_count = {SEED_COUNT}, max_hops = {MAX_HOPS}")
    print()

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
        default_top_k=TOP_K,
        max_hops=MAX_HOPS,
    )

    # Per-query results: {tc_id: {mode_name: per_mode_record}}
    per_query: dict[str, dict] = {}
    # Aggregate counters
    agg = {
        mode: {"citation_hits": 0, "citation_total": 0, "entity_hits": 0, "entity_total": 0, "pass": 0}
        for mode in ("vector_only", "graph_only", "hybrid_rrf")
    }
    cat_breakdown = defaultdict(lambda: {
        mode: {"score_sum": 0.0, "n": 0, "pass": 0}
        for mode in ("vector_only", "graph_only", "hybrid_rrf")
    })

    t_start = time.time()
    for tc in test_cases:
        print(f"--- {tc['id']} ({tc.get('category','?')}) ---")
        print(f"  Q: {tc['query'][:75]}...")

        query_embedding = engine._embed_query(tc["query"])

        # ---- Mode 1: vector_only ----
        v_results = engine._vector_search(
            query_embedding, GraphStore.VECTOR_COLLECTIONS, TOP_K, None,
        )
        v_ids = {r["entity_id"] for r in v_results[:TOP_K]}
        v_rec = score_mode(v_ids, tc["expected_citations"], tc["expected_entities"])

        # ---- Mode 2: graph_only (vector-seeded) ----
        seed_ids = [r["entity_id"] for r in v_results[:SEED_COUNT]]
        g_results = engine._graph_traverse(seed_ids=seed_ids, max_hops=MAX_HOPS)
        # Drop the seed IDs themselves so this is truly "graph expansion" not "vector + first-hop only"
        g_ids = {r["entity_id"] for r in g_results[:TOP_K]} - set(seed_ids)
        g_rec = score_mode(g_ids, tc["expected_citations"], tc["expected_entities"])

        # ---- Mode 3: hybrid_rrf (production path) ----
        h_results = engine.query(tc["query"], top_k=TOP_K)
        h_ids = {r["entity_id"] for r in h_results}
        h_rec = score_mode(h_ids, tc["expected_citations"], tc["expected_entities"])

        per_query[tc["id"]] = {"category": tc.get("category"), "vector_only": v_rec, "graph_only": g_rec, "hybrid_rrf": h_rec}

        # ---- Aggregate ----
        for mode, rec in (("vector_only", v_rec), ("graph_only", g_rec), ("hybrid_rrf", h_rec)):
            agg[mode]["citation_hits"] += len(rec["citation_hits"])
            agg[mode]["citation_total"] += len(tc["expected_citations"])
            agg[mode]["entity_hits"] += len(rec["entity_hits"])
            agg[mode]["entity_total"] += len(tc["expected_entities"])
            agg[mode]["pass"] += int(rec["pass"])
            cat = tc.get("category", "unknown")
            cat_breakdown[cat][mode]["score_sum"] += rec["score"]
            cat_breakdown[cat][mode]["n"] += 1
            cat_breakdown[cat][mode]["pass"] += int(rec["pass"])

        # ---- Per-query line ----
        def fmt(rec):
            cit = f"{len(rec['citation_hits'])}/{len(tc['expected_citations'])}"
            ent = f"{len(rec['entity_hits'])}/{len(tc['expected_entities'])}"
            return f"cit {cit}, ent {ent}, score {rec['score']:.0%}{' PASS' if rec['pass'] else ' FAIL'}"
        print(f"  vec : {fmt(v_rec)}")
        print(f"  grph: {fmt(g_rec)}")
        print(f"  hyb : {fmt(h_rec)}")
        print()

    duration = time.time() - t_start

    # ---- Final summary ----
    n = len(test_cases)
    print("=" * 70)
    print("AGGREGATE — citation recall@15 / entity recall@15 / pass rate")
    print("=" * 70)
    print(f"  {'Mode':<14}  {'Citation':<14}  {'Entity':<14}  {'Pass rate':<12}")
    print(f"  {'-' * 14}  {'-' * 14}  {'-' * 14}  {'-' * 12}")
    for mode in ("vector_only", "graph_only", "hybrid_rrf"):
        a = agg[mode]
        cit = f"{a['citation_hits']:>2}/{a['citation_total']:<2} ({100*a['citation_hits']/max(a['citation_total'],1):>5.1f}%)"
        ent = f"{a['entity_hits']:>2}/{a['entity_total']:<2} ({100*a['entity_hits']/max(a['entity_total'],1):>5.1f}%)"
        pas = f"{a['pass']:>2}/{n:<2} ({100*a['pass']/n:>5.1f}%)"
        print(f"  {mode:<14}  {cit:<14}  {ent:<14}  {pas:<12}")
    print()

    print("=" * 70)
    print("BY CATEGORY — mean retrieval score per mode")
    print("=" * 70)
    print(f"  {'Category':<16}  {'n':<3}  {'vec':<7}  {'grph':<7}  {'hyb':<7}")
    for cat in ("single_hop", "multi_hop", "out_of_scope"):
        cs = cat_breakdown.get(cat)
        if not cs:
            continue
        n_cat = cs["vector_only"]["n"]
        v = f"{100*cs['vector_only']['score_sum']/max(n_cat,1):.0f}%"
        g = f"{100*cs['graph_only']['score_sum']/max(n_cat,1):.0f}%"
        h = f"{100*cs['hybrid_rrf']['score_sum']/max(n_cat,1):.0f}%"
        print(f"  {cat:<16}  {n_cat:<3}  {v:<7}  {g:<7}  {h:<7}")
    print()
    print(f"Total wall-clock: {duration:.1f}s ({duration/n:.2f}s per query)")

    # ---- Write artifact ----
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    artifact = {
        "timestamp_utc": ts,
        "n_queries": n,
        "top_k": TOP_K,
        "seed_count": SEED_COUNT,
        "max_hops": MAX_HOPS,
        "aggregate": agg,
        "category_breakdown": {cat: dict(cb) for cat, cb in cat_breakdown.items()},
        "per_query": per_query,
        "wall_clock_seconds": duration,
        "neo4j_uri": settings.neo4j_uri,
    }
    out_path = OUT_DIR / f"three_mode_results_{ts}.json"
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\nArtifact written: {out_path}")

    graph.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
