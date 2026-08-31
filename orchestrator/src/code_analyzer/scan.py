"""Scan entry point: clone -> scan -> profile -> enrich via KG."""

from __future__ import annotations

import logging
from pathlib import Path

from src.code_analyzer.ingest import IngestResult, ingest, ingest_local
from src.code_analyzer.llm_ast_reviewer import review_decision_surfaces
from src.code_analyzer.models import AISystemProfile
from src.code_analyzer.profile import build_profile
from src.code_analyzer.rule_loader import load_rules
from src.code_analyzer.scanners import (
    AstRulesScanner,
    AstScanner,
    ContentScanner,
    CooccurrenceScanner,
    FilePatternScanner,
    ImportScanner,
    ScanContext,
)

logger = logging.getLogger(__name__)


async def run_scan(
    scan_id: str,
    repo_url: str | None = None,
    ref: str = "main",
    local_path: Path | None = None,
    enrich_with_kg: bool = True,
) -> AISystemProfile:
    if local_path is not None:
        result: IngestResult = ingest_local(local_path)
    elif repo_url:
        result = ingest(repo_url, ref=ref)
    else:
        raise ValueError("Either repo_url or local_path must be provided")

    try:
        profile = _scan_and_profile(scan_id, result)
    finally:
        result.cleanup()

    # KG enrichment is now the LegalResearchAgent's job (runs inside the
    # supervisor). `enrich_with_kg` is preserved in the signature for
    # backwards compatibility with any caller that still passes it.
    _ = enrich_with_kg
    return profile


def _scan_and_profile(
    scan_id: str, result: IngestResult, use_llm: bool = True
) -> AISystemProfile:
    """`use_llm=False` skips the surface-review LLM pass entirely.

    The detection benchmark needs bit-for-bit reproducible runs with no API
    key and no cost; the fail-open LLM pass is nondeterministic on both
    counts. Production scans keep the default.
    """
    rules = load_rules()
    ctx = ScanContext(
        repo_root=result.repo_root,
        files=result.files,
        suppressions=result.suppressions,
    )
    # ORDER MATTERS: imports first (populates shared state for later scanners),
    # then AST (collects decision_surfaces), then LLM review of those surfaces,
    # then AST rules (uses the enriched surfaces), then content (emits
    # pii_fields), then file-patterns, then cooccurrence last.
    pipeline = [
        ImportScanner(),
        AstScanner(),
        AstRulesScanner(),
        ContentScanner(),
        FilePatternScanner(),
        CooccurrenceScanner(),
    ]
    all_findings = []
    for scanner in pipeline:
        if isinstance(scanner, AstRulesScanner) and use_llm:
            # LLM pass sits between surface collection and rule application.
            _llm_enrich_surfaces(ctx)
        try:
            all_findings.extend(scanner.scan(ctx, rules))
        except Exception as e:  # noqa: BLE001
            logger.exception("Scanner %s failed: %s", scanner.__class__.__name__, e)
    if use_llm:
        # v07 T2.2 — judge, never detector: may confirm or demote findings,
        # never create/delete/boost. Fail-open with a receipt in stats.
        from src.code_analyzer.finding_triage import triage_findings

        ctx.shared["llm_triage"] = triage_findings(all_findings)
    else:
        ctx.shared["llm_triage"] = {"status": "skipped", "reason": "use_llm=False"}
    return build_profile(
        scan_id=scan_id,
        repo_info=result.repo_info,
        findings=all_findings,
        shared=ctx.shared,
    )


def _llm_enrich_surfaces(ctx: ScanContext) -> None:
    """Run the LLM reviewer over collected surfaces and drop test/mock ones.

    Fail-open: on any failure ``review_decision_surfaces`` returns the
    originals with ``is_test_or_mock=False``, so rule application still
    proceeds with the regex verdicts.
    """
    surfaces: list = ctx.shared.get("decision_surfaces", [])
    if not surfaces:
        return
    try:
        enriched = review_decision_surfaces(surfaces, ctx.repo_root)
    except Exception as e:  # noqa: BLE001
        logger.warning("LLM AST review failed, keeping regex verdicts: %s", e)
        return
    kept = [s for s in enriched if not s.get("is_test_or_mock")]
    dropped = len(enriched) - len(kept)
    if dropped:
        logger.info("LLM AST review dropped %d test/mock surface(s)", dropped)
    ctx.shared["decision_surfaces"] = kept
