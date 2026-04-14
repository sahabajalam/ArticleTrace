"""Semantic review of AST-extracted decision surfaces.

The AST scanner uses tree-sitter to find routes that look like decision
surfaces, then relies on regex (`HUMAN_REVIEW_KEYWORDS`, `AUDIT_KEYWORDS`,
`INFERENCE_CALL_PATTERNS`) to decide whether each one actually calls a
model, has human review, and has audit logging. That's brittle — it misses
custom wrappers, mislabels test routes, and can't tell a health-check from
a real inference endpoint.

This module sends each surface's code window to `gemini-2.5-flash-lite`
and overwrites the three boolean flags with the LLM's judgement, plus
`is_test_or_mock` so the caller can drop test/mock surfaces before rule
application.

Fail-open by design: any LLM failure leaves the original regex verdict in
place so the scan still produces findings.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from pathlib import Path
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import settings

logger = logging.getLogger(__name__)

WINDOW_BEFORE = 3
WINDOW_AFTER = 25


SYSTEM_PROMPT = """You are a code auditor for EU AI Act compliance scans.

You will be given JSON describing N candidate "decision surfaces" — HTTP
routes that a static scanner thinks might invoke an ML/AI model. For each
surface you get: a code window (~30 lines), the file path, the line
number, and the scanner's regex-based guesses.

Your job: return a strict JSON array with one object per input, in the
same order. For each item decide:

  - calls_model (bool): does this endpoint actually call an ML model,
    LLM, or AI service? (regexes can false-positive on names like
    `predict_date`, `classify_email_label`.)
  - has_human_review (bool): is there a human-review / approval /
    override hook before the decision is applied?
  - has_audit_log (bool): is the decision (or its inputs/outputs) logged
    to an audit trail? Plain debug logging is NOT audit.
  - is_test_or_mock (bool): is this code a test, mock, fixture, example,
    demo, or health check — i.e. not a real production decision path?
  - rationale (string, <=120 chars): one-line reason for your flags.

Return ONLY a JSON object of the form:
  {"items": [{"calls_model": ..., "has_human_review": ..., "has_audit_log": ..., "is_test_or_mock": ..., "rationale": "..."}, ...]}

Do not wrap in markdown fences. Do not add commentary."""


_json_block = re.compile(r"\{.*\}", re.DOTALL)


def review_decision_surfaces(
    surfaces: list[dict[str, Any]],
    repo_root: Path,
) -> list[dict[str, Any]]:
    """Return a new list of surfaces with LLM-refined flags.

    Drops nothing — callers decide whether to drop `is_test_or_mock` entries.
    On any failure the original surface is returned unchanged but with
    `is_test_or_mock=False` so downstream rules behave as before.
    """
    if not surfaces:
        return surfaces

    capped = surfaces[: settings.ast_reviewer_max_surfaces]
    skipped = len(surfaces) - len(capped)
    if skipped:
        logger.info("ast_reviewer: capped at %d surfaces (%d skipped)", len(capped), skipped)

    try:
        llm = ChatGoogleGenerativeAI(
            model=settings.ast_reviewer_model,
            google_api_key=settings.gemini_api_key,
            temperature=0.0,
        )
    except Exception as e:  # noqa: BLE001
        logger.warning("ast_reviewer: LLM init failed, keeping regex verdicts: %s", e)
        return [_with_default_flags(s) for s in surfaces]

    enriched: list[dict[str, Any]] = []
    batch_size = max(1, settings.ast_reviewer_batch_size)
    for start in range(0, len(capped), batch_size):
        batch = capped[start : start + batch_size]
        batch_payload = [_build_payload(s, repo_root) for s in batch]
        verdicts = _call_llm(llm, batch_payload)
        if verdicts is None or len(verdicts) != len(batch):
            # fail-open: pass original flags through
            enriched.extend(_with_default_flags(s) for s in batch)
            continue
        for surface, verdict in zip(batch, verdicts):
            enriched.append(_apply_verdict(surface, verdict))

    # Any surfaces beyond the cap keep their original flags.
    for s in surfaces[len(capped):]:
        enriched.append(_with_default_flags(s))
    return enriched


def _build_payload(surface: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    file_rel = surface.get("file", "")
    line = int(surface.get("line", 1))
    window, window_hash = _read_window(repo_root / file_rel, line)
    return {
        "endpoint": surface.get("endpoint", "?"),
        "file": file_rel,
        "line": line,
        "regex_verdict": {
            "calls_model": bool(surface.get("calls_model")),
            "has_human_review": bool(surface.get("has_human_review")),
            "has_audit_log": bool(surface.get("has_audit_log")),
        },
        "code_window": window,
        "_hash": window_hash,
    }


def _read_window(path: Path, line_1indexed: int) -> tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return "", ""
    lines = text.splitlines()
    start = max(0, line_1indexed - 1 - WINDOW_BEFORE)
    end = min(len(lines), line_1indexed - 1 + WINDOW_AFTER)
    snippet = "\n".join(lines[start:end])
    digest = hashlib.sha256(snippet.encode("utf-8", errors="replace")).hexdigest()[:12]
    return snippet, digest


def _call_llm(llm: ChatGoogleGenerativeAI, payload: list[dict[str, Any]]) -> list[dict[str, Any]] | None:
    user_msg = json.dumps({"surfaces": payload}, ensure_ascii=False)
    prompt = f"{SYSTEM_PROMPT}\n\nINPUT:\n{user_msg}"
    try:
        response = llm.invoke(prompt)
    except Exception as e:  # noqa: BLE001
        logger.warning("ast_reviewer: LLM call failed: %s", e)
        return None

    text = response.content if hasattr(response, "content") else str(response)
    if isinstance(text, list):  # some providers return list of parts
        text = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in text)
    match = _json_block.search(text or "")
    if not match:
        logger.warning("ast_reviewer: no JSON in LLM response")
        return None
    try:
        obj = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        logger.warning("ast_reviewer: JSON decode failed: %s", e)
        return None

    items = obj.get("items")
    if not isinstance(items, list):
        logger.warning("ast_reviewer: missing 'items' array")
        return None
    return items


def _apply_verdict(surface: dict[str, Any], verdict: dict[str, Any]) -> dict[str, Any]:
    out = dict(surface)
    for key in ("calls_model", "has_human_review", "has_audit_log"):
        val = verdict.get(key)
        if isinstance(val, bool):
            out[key] = val
    out["is_test_or_mock"] = bool(verdict.get("is_test_or_mock", False))
    rationale = verdict.get("rationale")
    if isinstance(rationale, str):
        out["llm_rationale"] = rationale[:200]
    out["llm_reviewed"] = True
    return out


def _with_default_flags(surface: dict[str, Any]) -> dict[str, Any]:
    out = dict(surface)
    out.setdefault("is_test_or_mock", False)
    out.setdefault("llm_reviewed", False)
    return out
