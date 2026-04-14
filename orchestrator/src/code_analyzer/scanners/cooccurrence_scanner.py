"""Co-occurrence rule: fires when another rule's findings co-locate with
keyword hits in the same file (e.g. biometric lib + 'public/cctv/street').
"""

from __future__ import annotations

import re
from pathlib import Path

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext


class CooccurrenceScanner(Scanner):
    technique = "cooccurrence"

    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        applicable = self.applicable_rules(rules)
        if not applicable:
            return []
        imports_by_rule = ctx.shared.get("imports_by_rule", {}) or {}
        findings: list[Finding] = []
        for rule in applicable:
            requires_rule: str | None = rule.patterns.get("requires_rule")
            keywords: list[str] = rule.patterns.get("keywords", []) or []
            window_lines: int = int(rule.patterns.get("within_lines", 200))
            if not requires_rule or not keywords:
                continue
            if requires_rule not in imports_by_rule:
                continue
            regex = re.compile(
                "|".join(rf"\b{re.escape(k)}\b" for k in keywords), re.IGNORECASE
            )
            for rel, matches in imports_by_rule[requires_rule]:
                try:
                    text = (ctx.repo_root / rel).read_text(
                        encoding="utf-8", errors="replace"
                    )
                except OSError:
                    continue
                lines = text.splitlines()
                for sym, line_no, excerpt in matches:
                    start = max(0, line_no - 1 - window_lines)
                    end = min(len(lines), line_no + window_lines)
                    chunk = "\n".join(lines[start:end])
                    m = regex.search(chunk)
                    if not m:
                        continue
                    sup, reason = ctx.is_suppressed(rule.id, rel)
                    conf = self.apply_dampeners(rule, rel, rule.base_confidence)
                    ev = [
                        Evidence(
                            file=rel, line=line_no, excerpt=excerpt, symbol=sym
                        ),
                        Evidence(
                            file=rel, line=line_no, symbol=m.group(0),
                            excerpt=f"co-occurring keyword '{m.group(0)}'",
                        ),
                    ]
                    f = self.build_finding(rule, ev, confidence=conf)
                    f.suppressed, f.suppress_reason = sup, reason
                    findings.append(f)
                    break  # one per file is enough
        return findings
