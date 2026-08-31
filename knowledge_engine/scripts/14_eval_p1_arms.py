"""Ablation for the v08 P1 retrieval arms — name index and COMPLEMENTS.

Runs the 25-query golden set under four configurations so each arm's effect
is attributable rather than assumed:

  baseline      both arms off — must reproduce the committed METRICS.md numbers
  name_only     lexical name arm added to RRF
  complements   one-hop COMPLEMENTS expansion off the vector hits
  both          production configuration

NORTHSTAR estimated entity recall 25% -> ~46% and multi-hop 46% -> ~55%.
Those are hypotheses; this script is what decides whether they hold. Report
whatever it prints, including a regression.

Usage:
  cd knowledge_engine
  ./.venv/bin/python scripts/14_eval_p1_arms.py [--out results.json]
  # Windows: ./.venv/Scripts/python.exe scripts/14_eval_p1_arms.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import settings  # noqa: E402
from src.retrieval.engine import RetrievalEngine  # noqa: E402
from src.stores.graph_store import GraphStore  # noqa: E402

from google import genai  # noqa: E402

TOP_K = 15
GOLDEN = PROJECT_ROOT / "golden_tests" / "test_queries.json"

CONFIGS = {
    "baseline":    {"use_name_arm": False, "use_complements": False},
    "name_only":   {"use_name_arm": True,  "use_complements": False},
    "complements": {"use_name_arm": False, "use_complements": True},
    "both":        {"use_name_arm": True,  "use_complements": True},
}


def load_cases() -> list[dict]:
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("queries", [])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    cases = load_cases()
    graph = GraphStore(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
    if not graph.name_index_exists():
        print("[eval] name index missing — run graph.create_name_index() first")
        return 2
    client = genai.Client(api_key=settings.google_api_key)
    engine = RetrievalEngine(
        graph_store=graph, genai_client=client,
        rrf_k=settings.rrf_k, default_top_k=TOP_K, max_hops=settings.max_hops,
    )

    results: dict[str, dict] = {}
    per_query: dict[str, dict] = {}

    for name, flags in CONFIGS.items():
        engine.use_name_arm = flags["use_name_arm"]
        engine.use_complements = flags["use_complements"]

        cit_hit = cit_tot = ent_hit = ent_tot = passes = 0
        by_cat: dict[str, list[float]] = {}

        for tc in cases:
            ids = {r["entity_id"] for r in engine.query(tc["query"], top_k=TOP_K)}
            exp_c = tc.get("expected_citations") or []
            exp_e = tc.get("expected_entities") or []
            ch = [c for c in exp_c if c in ids]
            eh = [e for e in exp_e if e in ids]
            cit_hit += len(ch); cit_tot += len(exp_c)
            ent_hit += len(eh); ent_tot += len(exp_e)
            score = (len(ch) + len(eh)) / max(len(exp_c) + len(exp_e), 1)
            if score >= 0.5:
                passes += 1
            by_cat.setdefault(tc.get("category", "?"), []).append(score)
            per_query.setdefault(tc["id"], {})[name] = {
                "score": round(score, 3),
                "citation_miss": [c for c in exp_c if c not in ids],
                "entity_miss": [e for e in exp_e if e not in ids],
            }

        results[name] = {
            "citation_recall": round(cit_hit / max(cit_tot, 1), 4),
            "citation": f"{cit_hit}/{cit_tot}",
            "entity_recall": round(ent_hit / max(ent_tot, 1), 4),
            "entity": f"{ent_hit}/{ent_tot}",
            "pass_rate": round(passes / max(len(cases), 1), 4),
            "passes": f"{passes}/{len(cases)}",
            "by_category": {k: round(sum(v) / len(v), 4) for k, v in by_cat.items()},
        }
        r = results[name]
        print(f"[eval] {name:12} citation {r['citation']:>7} ({r['citation_recall']:.1%})  "
              f"entity {r['entity']:>7} ({r['entity_recall']:.1%})  "
              f"pass {r['passes']:>6} ({r['pass_rate']:.0%})")

    base, both = results["baseline"], results["both"]
    print("\n[eval] delta (both vs baseline):")
    for metric in ("citation_recall", "entity_recall", "pass_rate"):
        d = both[metric] - base[metric]
        print(f"         {metric:16} {base[metric]:.1%} -> {both[metric]:.1%}  ({d:+.1%})")
    print("       by category:")
    for cat in sorted(base["by_category"]):
        b, t = base["by_category"][cat], both["by_category"].get(cat, 0)
        print(f"         {cat:14} {b:.0%} -> {t:.0%}  ({t - b:+.0%})")

    graph.close()
    if args.out:
        Path(args.out).write_text(json.dumps(
            {"configs": results, "per_query": per_query}, indent=2))
        print(f"\n[eval] wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
