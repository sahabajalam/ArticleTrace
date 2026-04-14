"""Presence/absence of marker files at repo level.

Used for transparency / DPIA / data-card rules. Fires on ABSENCE — only
once per scan — when a pre-condition is met (e.g. the repo uses an LLM
SDK but has no model_card.md).
"""

from __future__ import annotations

import re
from pathlib import Path

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext


class FilePatternScanner(Scanner):
    technique = "file_pattern"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        applicable = self.applicable_rules(rules)
        if not applicable:
            return []
        findings: list[Finding] = []
        # repo-level file list (names + relative paths, case-insensitive)
        rel_paths = {ctx.rel(p).lower() for p in ctx.files}

        for rule in applicable:
            mode = rule.patterns.get("mode", "absent")  # absent | present
            markers: list[str] = rule.patterns.get("markers", []) or []
            requires_any: list[str] = rule.patterns.get("requires_any_rule", []) or []

            # If a precondition rule_id set is specified, at least one such
            # finding must already exist (e.g. LLM SDK detected before we
            # flag missing model card).
            imports_by_rule = ctx.shared.get("imports_by_rule", {}) or {}
            if requires_any and not any(rid in imports_by_rule for rid in requires_any):
                continue

            # Check markers against repo file list.
            found_marker = any(_path_match(m.lower(), rel_paths) for m in markers)
            triggered = (mode == "absent" and not found_marker) or (
                mode == "present" and found_marker
            )
            if not triggered:
                continue

            sup, reason = ctx.is_suppressed(rule.id, "<repo>")
            # An absent-marker finding is a repo-level fact (e.g. "no
            # model_card.md anywhere"), so point evidence at the repo root
            # rather than borrowing a file from the precondition rule —
            # which previously caused misleading rows like
            # `tests/test_biometric.py:11` for AI-004 / AI-006.
            #
            # For mode=present the marker IS the evidence, so use the
            # matched marker file (best-effort) when we can find it; fall
            # back to a precondition pointer as before.
            ev: list[Evidence] = []
            if mode == "absent":
                ev.append(
                    Evidence(
                        file=".",
                        line=0,
                        excerpt=f"Missing repo-level documentation: expected one of {', '.join(markers)}",
                        symbol="<repo>",
                    )
                )
            else:
                marker_ev = _first_marker_evidence(markers, rel_paths)
                if marker_ev:
                    ev.append(marker_ev)
                else:
                    precondition_ev = _first_precondition_evidence(
                        imports_by_rule, requires_any, ctx
                    )
                    if precondition_ev:
                        ev.append(precondition_ev)
                    else:
                        ev.append(
                            Evidence(
                                file=".",
                                line=0,
                                excerpt=f"Marker present: {', '.join(markers)}",
                                symbol="<repo>",
                            )
                        )
            conf = rule.base_confidence
            f = self.build_finding(rule, ev, confidence=conf)
            f.suppressed, f.suppress_reason = sup, reason
            findings.append(f)
        return findings


def _first_marker_evidence(
    markers: list[str], rel_paths: set[str]
) -> Evidence | None:
    """Return an Evidence row pointing at the first matched marker file."""
    for m in markers:
        ml = m.lower()
        for p in rel_paths:
            if p == ml or p.endswith("/" + ml) or p.endswith("\\" + ml):
                return Evidence(file=p, line=1, excerpt=f"Marker file present: {m}")
    return None


def _path_match(marker: str, rel_paths: set[str]) -> bool:
    # Plain filename at any depth OR exact path
    if "/" in marker or "\\" in marker:
        return marker in rel_paths
    # else: match basename anywhere
    for p in rel_paths:
        if p == marker or p.endswith("/" + marker):
            return True
    return False


def _first_precondition_evidence(
    imports_by_rule: dict, requires_any: list[str], ctx: ScanContext
) -> Evidence | None:
    for rid in requires_any:
        hits = imports_by_rule.get(rid)
        if not hits:
            continue
        rel, matches = hits[0]
        if matches:
            sym, line, excerpt = matches[0]
            return Evidence(file=rel, line=line, excerpt=excerpt, symbol=sym)
    return None
