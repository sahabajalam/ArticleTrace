"""LLM triage of scanner findings — judge, never detector (v07 T2.2).

IRIS-shaped (arxiv 2405.17238): the deterministic scanners remain the only
source of findings; the LLM reviews each candidate and may CONFIRM it or
DEMOTE it (vendored code, dead code, generated files, docs tooling — things
path heuristics cannot see). The contract is one-directional by construction:

  - never creates a finding
  - never deletes a finding
  - never raises confidence
  - demotion halves confidence and records the reason on the finding

so every reported finding is still traceable to a YAML rule and a code
anchor (NORTHSTAR Part V), and a hallucinated triage verdict can only make
the scan *quieter*, never invent risk.

Interaction with T2.1: demoting a prohibited-trigger finding below
PROHIBITED_MIN_CONFIDENCE means the risk classifier will not escalate on it —
the LLM can defuse a dubious PROHIBITED, never cause one.

Fail-open with a receipt: any LLM failure leaves findings untouched and the
outcome (ok / skipped / failed, counts, cap) is reported in
`stats.llm_triage` — a scan must show whether triage actually ran (v07 §5).
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from src.config import settings

logger = logging.getLogger(__name__)

# Bounded cost per scan. The cap is reported, never silent: 200 findings in,
# 40 reviewed, stats say so.
MAX_TRIAGE_FINDINGS = 40
DEMOTION_FACTOR = 0.5

_JSON_BLOCK = re.compile(r"\{.*\}", re.DOTALL)

SYSTEM_PROMPT = """You are triaging static-analysis findings for an EU AI Act
compliance scan. Each finding was produced by a deterministic rule and cites
real code evidence. Your ONLY job is to judge, per finding, whether the cited
code is genuine use inside this project's own shipped code, or something a
path heuristic cannot classify: vendored/third-party code copied into the
repo, dead or commented-out code, generated files, documentation tooling, or
demo/sample material.

Return STRICT JSON: {"items": [{"index": <int>, "verdict": "confirmed" |
"demoted", "reason": "<one short sentence>"}, ...]} — one object per input
index, no other text. When unsure, answer "confirmed": you may only weaken a
finding for a reason you can state."""


def apply_triage(findings: list[Any], items: list[dict[str, Any]]) -> dict[str, int]:
    """Apply LLM verdicts to findings, enforcing the one-directional contract.

    Pure and defensive: unknown indices, duplicate indices, malformed rows and
    unknown verdicts are ignored (counted), because this input crosses an LLM
    boundary. Returns counters for the stats report.
    """
    counters = {"confirmed": 0, "demoted": 0, "ignored": 0}
    seen: set[int] = set()
    for row in items:
        if not isinstance(row, dict):
            counters["ignored"] += 1
            continue
        idx = row.get("index")
        verdict = row.get("verdict")
        if not isinstance(idx, int) or idx < 0 or idx >= len(findings) or idx in seen:
            counters["ignored"] += 1
            continue
        seen.add(idx)
        f = findings[idx]
        if verdict == "confirmed":
            counters["confirmed"] += 1
            f.triage = "llm-confirmed"
        elif verdict == "demoted":
            counters["demoted"] += 1
            reason = str(row.get("reason") or "no reason given")[:200]
            f.confidence = round(f.confidence * DEMOTION_FACTOR, 2)
            f.triage = f"llm-demoted: {reason}"
        else:
            counters["ignored"] += 1
    return counters


def triage_findings(findings: list[Any]) -> dict[str, Any]:
    """Run the LLM over up to MAX_TRIAGE_FINDINGS findings. Returns the
    stats report; mutates findings in place per apply_triage."""
    candidates = [f for f in findings if not f.suppressed]
    if not candidates:
        return {"status": "skipped", "reason": "no findings", "reviewed": 0}

    batch = candidates[:MAX_TRIAGE_FINDINGS]
    capped = len(candidates) - len(batch)
    payload = [
        {
            "index": i,
            "rule_id": f.rule_id,
            "title": f.title,
            "confidence": f.confidence,
            "evidence": [
                {"file": e.file, "line": e.line, "excerpt": (e.excerpt or "")[:200]}
                for e in f.evidence[:2]
            ],
        }
        for i, f in enumerate(batch)
    ]

    items = _call_llm(payload)
    if items is None:
        return {
            "status": "failed",
            "reason": "LLM call or parse failed — findings unchanged",
            "reviewed": 0,
            "capped_out": capped,
        }

    counters = apply_triage(batch, items)
    report = {"status": "ok", "reviewed": len(batch), "capped_out": capped, **counters}
    logger.info("finding triage: %s", report)
    return report


def _call_llm(payload: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI

        llm = ChatGoogleGenerativeAI(
            model=settings.ast_reviewer_model,
            temperature=0.0,
            google_api_key=settings.gemini_api_key,
        )
        prompt = f"{SYSTEM_PROMPT}\n\nINPUT:\n{json.dumps({'findings': payload}, ensure_ascii=False)}"
        response = llm.invoke(prompt)
        text = response.content if isinstance(response.content, str) else str(response.content)
        match = _JSON_BLOCK.search(text or "")
        if not match:
            return None
        obj = json.loads(match.group(0))
        items = obj.get("items")
        return items if isinstance(items, list) else None
    except Exception as e:  # noqa: BLE001 — fail-open, reported by caller
        logger.warning("finding triage failed open: %s", e)
        return None
