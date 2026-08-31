"""Regex content scan over docstrings, README, and identifier names.

Used for prohibited-practice keywords (AI-008) and PII field detection (AI-005).
"""

from __future__ import annotations

import re
from pathlib import Path

from src.code_analyzer.models import Evidence, Finding
from src.code_analyzer.rule_loader import RuleSpec
from src.code_analyzer.scanners.base import Scanner, ScanContext
from src.code_analyzer.source_reader import read_source_bytes


TEXT_EXTS = {".py", ".ipynb", ".js", ".jsx", ".ts", ".tsx", ".md", ".rst", ".txt", ".yaml", ".yml"}
# `strings:` patterns (model ids, hosted-LLM endpoints — v07 T1.3) scan CODE
# only. Prose mentioning api.openai.com in a README is documentation, not
# usage; matching it would re-create the DL-030 class of false positive.
CODE_EXTS = {".py", ".ipynb", ".js", ".jsx", ".ts", ".tsx"}
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
        # A rule belongs to one primary technique, but any rule may carry an
        # auxiliary `strings:` signal (v07 T1.3) — e.g. AI-002 is import_scan,
        # yet raw-HTTP calls to api.openai.com are content evidence. Routing
        # only by technique made the string patterns unreachable.
        seen = {r.id for r in applicable}
        applicable = applicable + [
            r for r in rules
            if r.id not in seen and (r.patterns.get("strings") or [])
        ]
        if not applicable:
            return []
        findings: list[Finding] = []
        pii_bucket: set[str] = set()
        imports_by_rule: dict = ctx.shared.get("imports_by_rule", {})
        for rule in applicable:
            # Same precondition gate FilePatternScanner honours: a content rule
            # can declare it only makes sense once other rules found AI usage.
            # Without this, AI-005 fired on the word "email" in a docstring of
            # a web framework with zero AI anywhere (benchmark FP on
            # pallets/flask) — bare PII keywords are not an AI system.
            requires_any: list[str] = rule.patterns.get("requires_any_rule", []) or []
            if requires_any and not any(rid in imports_by_rule for rid in requires_any):
                continue
            patterns: list[str] = rule.patterns.get("keywords", []) or []
            string_patterns: list[str] = rule.patterns.get("strings", []) or []
            scope_exts = set(rule.patterns.get("extensions", list(TEXT_EXTS)))
            is_pii_rule = rule.patterns.get("collect_pii", False)
            if string_patterns:
                findings.extend(
                    self._string_pass(ctx, rule, string_patterns)
                )
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
                source, read_err = read_source_bytes(path)
                if read_err:
                    ctx.shared.setdefault("source_read_errors", []).append(read_err)
                if not source:
                    continue
                text = source.decode("utf-8", errors="replace")
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


# appended by v07 T1.3 — see CODE_EXTS note above
def _compile_strings(patterns: list[str]) -> "re.Pattern":
    return re.compile("|".join(f"(?:{p})" for p in patterns))


def _string_pass_impl(ctx, rule, string_patterns, scanner):
    from src.code_analyzer.models import Evidence
    from src.code_analyzer.source_reader import read_source_bytes

    regex = _compile_strings(string_patterns)
    rule_evidence: list[Evidence] = []
    for path in ctx.files:
        if path.suffix.lower() not in CODE_EXTS:
            continue
        source, read_err = read_source_bytes(path)
        if read_err:
            ctx.shared.setdefault("source_read_errors", []).append(read_err)
        if not source:
            continue
        text = source.decode("utf-8", errors="replace")
        rel = ctx.rel(path)
        per_file = 0
        for i, line in enumerate(text.splitlines(), start=1):
            m = regex.search(line)
            if not m:
                continue
            rule_evidence.append(Evidence(
                file=rel, line=i, excerpt=line.strip()[:200], symbol=m.group(0)[:80],
            ))
            per_file += 1
            if per_file >= MAX_EVIDENCE_PER_FILE:
                break
    if not rule_evidence:
        return []
    sup, reason = ctx.is_suppressed(rule.id, rule_evidence[0].file)
    conf = scanner.apply_dampeners(rule, rule_evidence[0].file, rule.base_confidence)
    f = scanner.build_finding(rule, rule_evidence[:10], confidence=conf)
    f.suppressed = sup
    f.suppress_reason = reason
    return [f]


ContentScanner._string_pass = (
    lambda self, ctx, rule, string_patterns: _string_pass_impl(ctx, rule, string_patterns, self)
)
