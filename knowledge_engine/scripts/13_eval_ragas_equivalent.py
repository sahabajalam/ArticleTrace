"""RAGAS-equivalent metrics computed bespoke with the Gemini judge.

Rather than installing the heavyweight `ragas` package (LangChain + OpenAI +
pandas), this script implements the three RAGAS metrics that don't need a
ground-truth answer, using direct Gemini calls. Cleaner: no framework dep,
same judge model as the production reasoning engine.

Metrics on hybrid_rrf retrieval over the 25-query golden set:

  - **context_relevance** (a.k.a. context_precision)
      For each of the top-K retrieved entities, ask the judge "is this
      relevant to the query?" — fraction relevant per query, then average.
      No reasoning call needed; pure retrieval-side metric.

  - **answer_relevance**
      Run the ReasoningEngine to generate an answer, then ask the judge
      "is this answer relevant to the question?" — Likert 1–5, normalised.
      Costs one reasoning + one judge call per query.

  - **faithfulness**
      Run the ReasoningEngine, decompose the answer into atomic claims,
      then ask the judge per claim "is this claim supported by the
      retrieved contexts?" — fraction supported per query, then average.
      Costs one reasoning + (1 + n_claims) judge calls per query.

Usage:
  cd knowledge_engine
  ./.venv/Scripts/python.exe scripts/13_eval_ragas_equivalent.py \\
      [--context-only] [--limit N]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GOLDEN_PATH = PROJECT_ROOT / "golden_tests" / "test_queries.json"
OUT_DIR = PROJECT_ROOT / "golden_tests"

TOP_K = 15
JUDGE_MODEL = "gemini-2.5-flash"  # cheap, fast, good enough for binary/Likert judging
                                  # (2.0-flash was deprecated 2026-06-19)


CONTEXT_RELEVANCE_PROMPT = """You are evaluating retrieval quality for a legal/regulatory question-answering system.

QUESTION:
{question}

RETRIEVED ENTITY:
- ID: {entity_id}
- Type: {entity_type}
- Content: {content}

Is this entity directly relevant to answering the question? "Relevant" means the entity provides legal text, definitions, obligations, rights, or regulatory context the answer would cite. Tangentially related is NOT relevant.

Respond with exactly one JSON object: {{"relevant": true | false, "reason": "<one short sentence>"}}"""


ANSWER_RELEVANCE_PROMPT = """You are evaluating answer quality for a legal/regulatory question-answering system.

QUESTION:
{question}

GENERATED ANSWER:
{answer}

How relevant is the answer to the question? Score on a 1–5 Likert scale:
  1 = unrelated / nonsense
  2 = tangentially related but doesn't address the question
  3 = partially addresses the question
  4 = addresses the question with minor gaps
  5 = directly and completely addresses the question

Respond with exactly one JSON object: {{"score": 1 | 2 | 3 | 4 | 5, "reason": "<one short sentence>"}}"""


FAITHFULNESS_DECOMPOSE_PROMPT = """Decompose this answer into atomic factual claims. Each claim should be one self-contained assertion that could be true or false.

ANSWER:
{answer}

Respond with exactly one JSON object: {{"claims": ["<claim 1>", "<claim 2>", ...]}}. Aim for 3–8 claims."""


FAITHFULNESS_VERIFY_PROMPT = """You are checking whether a factual claim is supported by source contexts.

CLAIM:
{claim}

CONTEXTS:
{contexts}

Is the claim directly supported by at least one of the contexts? "Supported" means the context explicitly states or directly implies the claim. Inference beyond what the contexts say is NOT support.

Respond with exactly one JSON object: {{"supported": true | false, "reason": "<one short sentence>"}}"""


def parse_json_response(text: str) -> dict | None:
    """Extract a JSON object from a possibly-fenced response."""
    if not text:
        return None
    # Strip markdown fences if any
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE)
    # Find the first {...} blob
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


_judge_errors: list[str] = []


def judge_call(genai_client, prompt: str, model: str = JUDGE_MODEL) -> str:
    """One Gemini judge call. Returns raw text. Records errors to a module-level list."""
    try:
        resp = genai_client.models.generate_content(
            model=model,
            contents=prompt,
        )
        return resp.text or ""
    except Exception as exc:
        err = f"{type(exc).__name__}: {str(exc)[:200]}"
        _judge_errors.append(err)
        if len(_judge_errors) <= 3:  # only print the first few
            print(f"    [judge_error] {err}")
        return ""


def get_entity_content(graph, entity_id: str) -> tuple[str, str]:
    """Fetch entity content text + type label for the judge.

    Property schema varies by node type — articles use `full_text` /
    `document_text`, concepts/rights use `description`, all have `title` or
    `name`. We coalesce in priority order, then prepend the title for context.
    """
    with graph._driver.session() as s:
        for r in s.run(
            "MATCH (n:Entity {id:$id}) RETURN labels(n) AS labels, "
            "n.full_text AS full_text, n.document_text AS document_text, "
            "n.description AS description, n.title AS title, n.name AS name LIMIT 1",
            id=entity_id,
        ):
            labels = [l for l in r["labels"] if l != "Entity"]
            entity_type = labels[0] if labels else "Entity"
            body = (
                r["full_text"] or r["document_text"]
                or r["description"] or r["title"] or r["name"] or "(no text)"
            )
            title = r["title"] or r["name"] or ""
            content = f"{title}\n\n{body}" if title and title != body else str(body)
            return entity_type, content[:2000]
    return "Entity", "(not found)"


def run_context_relevance(genai_client, graph, engine, test_cases: list[dict]) -> dict:
    """For each query, top-K hybrid retrieval → judge per entity → fraction relevant."""
    print("\n[1/3] CONTEXT RELEVANCE (hybrid_rrf, top-15)")
    print("-" * 70)
    per_query = {}
    relevant_counts = []
    for tc in test_cases:
        results = engine.query(tc["query"], top_k=TOP_K)
        relevant = 0
        non_relevant = 0
        details = []
        for r in results[:TOP_K]:
            eid = r["entity_id"]
            etype, content = get_entity_content(graph, eid)
            prompt = CONTEXT_RELEVANCE_PROMPT.format(
                question=tc["query"], entity_id=eid, entity_type=etype,
                content=content,
            )
            raw = judge_call(genai_client, prompt)
            parsed = parse_json_response(raw)
            if parsed and parsed.get("relevant") is True:
                relevant += 1
                details.append({"id": eid, "relevant": True})
            else:
                non_relevant += 1
                details.append({"id": eid, "relevant": False, "reason": (parsed or {}).get("reason", "")})
        total = relevant + non_relevant
        score = relevant / total if total else 0
        per_query[tc["id"]] = {"score": score, "relevant": relevant, "total": total, "details": details}
        relevant_counts.append(score)
        print(f"  {tc['id']:<35s}  {relevant}/{total} ({score:.0%})")
    overall = sum(relevant_counts) / len(relevant_counts)
    print(f"\n  Mean context relevance: {overall:.1%}")
    return {"metric": "context_relevance", "mean": overall, "per_query": per_query}


def run_answer_relevance(genai_client, reasoner, test_cases: list[dict]) -> dict:
    """For each query, generate answer via ReasoningEngine, judge relevance 1-5."""
    print("\n[2/3] ANSWER RELEVANCE (Likert 1-5, normalised)")
    print("-" * 70)
    from src.retrieval.query_models import ComplianceQueryRequest
    per_query = {}
    scores = []
    for tc in test_cases:
        try:
            req = ComplianceQueryRequest(
                question=tc["query"], max_results=TOP_K, include_reasoning=False,
            )
            resp = reasoner.answer(req)
            answer = resp.answer or "(empty)"
        except Exception as exc:
            answer = f"(reasoning_error: {type(exc).__name__})"
        raw = judge_call(genai_client, ANSWER_RELEVANCE_PROMPT.format(
            question=tc["query"], answer=answer,
        ))
        parsed = parse_json_response(raw)
        if parsed and isinstance(parsed.get("score"), int):
            likert = parsed["score"]
            normalised = (likert - 1) / 4  # 1 -> 0, 5 -> 1
        else:
            likert = None
            normalised = 0.0
        per_query[tc["id"]] = {
            "likert": likert, "normalised": normalised,
            "answer_preview": answer[:150],
            "reason": (parsed or {}).get("reason", ""),
        }
        scores.append(normalised)
        print(f"  {tc['id']:<35s}  Likert={likert} -> {normalised:.2f}")
    overall = sum(scores) / len(scores)
    print(f"\n  Mean answer relevance (normalised): {overall:.1%}")
    return {"metric": "answer_relevance", "mean": overall, "per_query": per_query}


def run_faithfulness(genai_client, reasoner, engine, graph, test_cases: list[dict]) -> dict:
    """For each query, generate answer, decompose to claims, judge each vs contexts."""
    print("\n[3/3] FAITHFULNESS (claims supported by contexts)")
    print("-" * 70)
    from src.retrieval.query_models import ComplianceQueryRequest
    per_query = {}
    per_query_scores = []
    for tc in test_cases:
        try:
            req = ComplianceQueryRequest(
                question=tc["query"], max_results=TOP_K, include_reasoning=False,
            )
            resp = reasoner.answer(req)
            answer = resp.answer or ""
        except Exception as exc:
            per_query[tc["id"]] = {"score": 0, "error": f"reasoning_error: {exc}"}
            per_query_scores.append(0)
            print(f"  {tc['id']:<35s}  REASONING FAILED: {exc}")
            continue

        if not answer.strip():
            per_query[tc["id"]] = {"score": 0, "claims": [], "note": "empty answer"}
            per_query_scores.append(0)
            print(f"  {tc['id']:<35s}  (empty answer)")
            continue

        # Build context block from top-K retrieval
        retrieval = engine.query(tc["query"], top_k=TOP_K)
        ctx_lines = []
        for r in retrieval[:TOP_K]:
            etype, content = get_entity_content(graph, r["entity_id"])
            ctx_lines.append(f"[{r['entity_id']}] ({etype})\n{content[:500]}")
        contexts_blob = "\n\n".join(ctx_lines)[:8000]  # cap

        # Decompose answer into claims
        raw = judge_call(genai_client, FAITHFULNESS_DECOMPOSE_PROMPT.format(answer=answer))
        parsed = parse_json_response(raw)
        claims = (parsed or {}).get("claims", [])[:8]
        if not claims:
            per_query[tc["id"]] = {"score": 0, "claims": [], "note": "no claims extracted"}
            per_query_scores.append(0)
            print(f"  {tc['id']:<35s}  (no claims extracted)")
            continue

        # Verify each claim
        supported = 0
        claim_details = []
        for claim in claims:
            v_raw = judge_call(genai_client, FAITHFULNESS_VERIFY_PROMPT.format(
                claim=claim, contexts=contexts_blob,
            ))
            v_parsed = parse_json_response(v_raw)
            is_supported = bool((v_parsed or {}).get("supported"))
            if is_supported:
                supported += 1
            claim_details.append({"claim": claim, "supported": is_supported})

        score = supported / len(claims)
        per_query[tc["id"]] = {
            "score": score, "supported": supported, "total": len(claims),
            "claims": claim_details,
        }
        per_query_scores.append(score)
        print(f"  {tc['id']:<35s}  {supported}/{len(claims)} ({score:.0%})")
    overall = sum(per_query_scores) / max(len(per_query_scores), 1)
    print(f"\n  Mean faithfulness: {overall:.1%}")
    return {"metric": "faithfulness", "mean": overall, "per_query": per_query}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context-only", action="store_true",
                        help="Run only context_relevance (no reasoning calls)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Run only the first N queries (smoke test)")
    args = parser.parse_args()

    from google import genai
    from src.config import settings
    from src.stores.graph_store import GraphStore
    from src.retrieval.engine import RetrievalEngine
    from src.retrieval.reasoning_engine import ReasoningEngine

    test_cases = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    if args.limit:
        test_cases = test_cases[:args.limit]
    print(f"Running RAGAS-equivalent metrics on {len(test_cases)} queries")
    print(f"Judge model: {JUDGE_MODEL}")
    print(f"Top-K: {TOP_K}")

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
        max_hops=2,
    )

    t0 = time.time()
    results = {"context_relevance": None, "answer_relevance": None, "faithfulness": None}

    results["context_relevance"] = run_context_relevance(genai_client, graph, engine, test_cases)

    if not args.context_only:
        reasoner = ReasoningEngine(
            retrieval_engine=engine,
            genai_client=genai_client,
            model=JUDGE_MODEL,
        )
        results["answer_relevance"] = run_answer_relevance(genai_client, reasoner, test_cases)
        results["faithfulness"] = run_faithfulness(genai_client, reasoner, engine, graph, test_cases)

    duration = time.time() - t0

    # ---- Summary ----
    print()
    print("=" * 70)
    print("RAGAS-EQUIVALENT METRIC SUMMARY")
    print("=" * 70)
    for metric, payload in results.items():
        if payload:
            print(f"  {metric:<22s} {payload['mean']:.1%}")
    print(f"\n  Wall clock: {duration:.1f}s ({duration/len(test_cases):.1f}s per query)")

    # ---- Write artifact ----
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    artifact = {
        "timestamp_utc": ts,
        "judge_model": JUDGE_MODEL,
        "n_queries": len(test_cases),
        "top_k": TOP_K,
        "wall_clock_seconds": duration,
        "neo4j_uri": settings.neo4j_uri,
        "results": results,
    }
    out_path = OUT_DIR / f"ragas_equiv_{ts}.json"
    out_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    print(f"\nArtifact written: {out_path}")

    graph.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
