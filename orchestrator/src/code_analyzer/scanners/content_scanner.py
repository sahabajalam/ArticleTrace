"""Regex content scan over docstrings, README, and identifier names.

Used for prohibited-practice keywords (AI-008) and PII field detection (AI-005).
"""

from __future__ import annotations

import re
from pathlib import Path

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext


TEXT_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".md", ".rst", ".txt", ".yaml", ".yml"}
MAX_EVIDENCE_PER_FILE = 3

_TEST_PATH_RE = re.compile(r"(^|/)(tests?|spec|specs|fixtures|examples?)/", re.IGNORECASE)


def _is_test_path(rel_path: str) -> bool:
    """True if a relative path lives under a tests/spec/fixtures/examples dir."""
    norm = rel_path.replace("\\", "/")
    return bool(_TEST_PATH_RE.search(norm))


class ContentScanner(Scanner):
    technique = "content_scan"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        applicable = self.applicable_rules(rules)
        if not applicable:
            return []
        findings: list[Finding] = []
        pii_bucket: set[str] = set()
        for rule in applicable:
            patterns: list[str] = rule.patterns.get("keywords", []) or []
            scope_exts = set(rule.patterns.get("extensions", list(TEXT_EXTS)))
            is_pii_rule = rule.patterns.get("collect_pii", False)
            if not patterns:
                continue
            regex = re.compile(
                "|".join(rf"\b{re.escape(p)}\b" for p in patterns),
                re.IGNORECASE,
            )
            rule_evidence: list[Evidence] = []
            for path in ctx.files:
                if path.suffix.lower() not in scope_exts:
                    continue
                try:
                    text = path.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                rel = ctx.rel(path)
                per_file = 0
                for i, line in enumerate(text.splitlines(), start=1):
                    m = regex.search(line)
                    if not m:
                        continue
                    rule_evidence.append(
                        Evidence(
                            file=rel,
                            line=i,
                            excerpt=line.strip()[:200],
                            symbol=m.group(0),
                        )
                    )
                    if is_pii_rule:
                        pii_bucket.add(m.group(0).lower())
                    per_file += 1
                    if per_file >= MAX_EVIDENCE_PER_FILE:
                        break
            if not rule_evidence:
                continue
            # Suppression at per-file granularity — collapse to one finding
            # with all evidence, filter suppressed entries.
            filtered: list[Evidence] = []
            sup_reasons: list[str] = []
            for ev in rule_evidence:
                sup, reason = ctx.is_suppressed(rule.id, ev.file)
                if sup:
                    if reason:
                        sup_reasons.append(reason)
                    continue
                filtered.append(ev)
            if not filtered:
                continue
            # Rank evidence so the canonical (first) row is the strongest signal,
            # not whichever file the OS happened to list first. Production files
            # outrank tests/specs; within the same tier, higher per-file match
            # density wins. The dampener is then computed from this canonical
            # file — so a 1-keyword test docstring no longer dampens a finding
            # whose real signal is in a 10-keyword production module.
            counts: dict[str, int] = {}
            for ev in filtered:
                counts[ev.file] = counts.get(ev.file, 0) + 1
            filtered.sort(
                key=lambda e: (_is_test_path(e.file), -counts.get(e.file, 0), e.file)
            )
            conf = self.apply_dampeners(rule, filtered[0].file, rule.base_confidence)
            f = self.build_finding(rule, filtered[:10], confidence=conf)
            findings.append(f)

        if pii_bucket:
            ctx.shared["pii_fields"] = sorted(pii_bucket)
        return findings
