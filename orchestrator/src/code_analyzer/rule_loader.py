"""Loads YAML rule definitions from rules/ into RuleSpec objects.

Rules are data, not code — mirrors Semgrep. Scanners read the spec at
runtime; adding a new rule = adding a YAML file.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

RULES_DIR = Path(__file__).parent / "rules"


@dataclass
class Dampener:
    when: str
    factor: float


@dataclass
class RuleSpec:
    id: str
    title: str
    severity: str
    technique: str  # import_scan | ast_scan | file_pattern | content_scan | cooccurrence
    languages: list[str]
    patterns: dict[str, Any]
    mapped_articles: list[str]
    obligation_anchors: list[str]
    remediation: str
    base_confidence: float = 0.9
    dampeners: list[Dampener] = field(default_factory=list)


def load_rules(rules_dir: Path | None = None) -> list[RuleSpec]:
    target = rules_dir or RULES_DIR
    rules: list[RuleSpec] = []
    for path in sorted(target.glob("*.yml")):
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        rules.append(_from_dict(data))
    return rules


def _from_dict(d: dict[str, Any]) -> RuleSpec:
    conf = d.get("confidence", {}) or {}
    dampeners = [Dampener(**x) for x in conf.get("dampeners", []) or []]
    maps_to = d.get("maps_to", {}) or {}
    return RuleSpec(
        id=d["id"],
        title=d["title"],
        severity=d["severity"],
        technique=d["technique"],
        languages=d.get("languages", ["python"]),
        patterns=d.get("patterns", {}) or {},
        mapped_articles=maps_to.get("articles", []) or [],
        obligation_anchors=maps_to.get("obligation_anchors", []) or [],
        remediation=d.get("remediation", ""),
        base_confidence=float(conf.get("base", 0.9)),
        dampeners=dampeners,
    )
