"""Scanner base class and shared scan context."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.code_analyzer.models import Evidence, Finding, Severity
from src.code_analyzer.rule_loader import RuleSpec


@dataclass
class ScanContext:
    """Shared state passed to every scanner for a single repo."""

    repo_root: Path
    files: list[Path]  # absolute paths, pre-filtered
    suppressions: list[dict[str, Any]] = field(default_factory=list)
    # scratch space scanners can write to (e.g. import-scanner records each
    # biometric lib hit so the cooccurrence scanner can pick it up)
    shared: dict[str, Any] = field(default_factory=dict)

    def rel(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.repo_root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

    def is_suppressed(self, rule_id: str, rel_path: str) -> tuple[bool, str | None]:
        for s in self.suppressions:
            if s.get("rule") != rule_id:
                continue
            pat = s.get("path")
            if pat and not _glob_match(pat, rel_path):
                continue
            return True, s.get("reason")
        return False, None


def _glob_match(pattern: str, path: str) -> bool:
    # Convert simple glob to regex (** = any, * = segment)
    regex = re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
    return re.fullmatch(regex, path) is not None


class Scanner(ABC):
    """ABC for all detection scanners."""

    #: Subclasses set the technique string they handle.
    technique: str = ""

    def applicable_rules(self, rules: list[RuleSpec]) -> list[RuleSpec]:
        return [r for r in rules if r.technique == self.technique]

    @abstractmethod
    def scan(self, ctx: ScanContext, rules: list[RuleSpec]) -> list[Finding]:
        ...

    # ---- helpers shared across subclasses -------------------------------

    @staticmethod
    def build_finding(
        rule: RuleSpec,
        evidence: list[Evidence],
        confidence: float | None = None,
        remediation: str | None = None,
    ) -> Finding:
        return Finding(
            rule_id=rule.id,
            title=rule.title,
            severity=Severity(rule.severity),
            confidence=confidence if confidence is not None else rule.base_confidence,
            evidence=evidence,
            mapped_articles=list(rule.mapped_articles),
            obligation_anchors=list(rule.obligation_anchors),
            remediation=remediation or rule.remediation,
        )

    @staticmethod
    def apply_dampeners(rule: RuleSpec, rel_path: str, base: float) -> float:
        conf = base
        for d in rule.dampeners:
            if _matches_when(d.when, rel_path):
                conf *= d.factor
        return max(0.0, min(1.0, conf))


def _matches_when(expr: str, rel_path: str) -> bool:
    """Mini DSL — supports 'file_matches: <regex>' for now."""
    expr = expr.strip()
    if expr.startswith("file_matches:"):
        pattern = expr.split(":", 1)[1].strip()
        return re.search(pattern, rel_path) is not None
    return False
