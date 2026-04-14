"""Domain models for the code analyzer.

These are the contract agents and the API surface depend on. Keep them
backward-compatible once wired.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Evidence(BaseModel):
    """One concrete code-level pointer that supports a finding."""

    file: str = Field(..., description="Repo-relative path")
    line: int = Field(..., ge=1, description="1-indexed line number")
    column: int | None = Field(None, ge=0)
    excerpt: str | None = Field(None, description="Short code excerpt, <=200 chars")
    symbol: str | None = Field(None, description="Import / identifier / keyword matched")


class Finding(BaseModel):
    """A single rule-match against the scanned repo."""

    rule_id: str = Field(..., description="e.g. AI-001")
    title: str
    severity: Severity
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: list[Evidence] = Field(default_factory=list)
    mapped_articles: list[str] = Field(
        default_factory=list,
        description="KG node IDs (AIACT_ART_5, GDPR_ART_9, ...)",
    )
    obligation_anchors: list[str] = Field(
        default_factory=list,
        description="Seed terms for KG hybrid retrieval",
    )
    remediation: str | None = None
    suppressed: bool = False
    suppress_reason: str | None = None


class AIComponent(BaseModel):
    """An AI/ML capability detected in the repo."""

    kind: Literal[
        "llm_sdk",
        "biometric_lib",
        "ml_framework",
        "vector_store",
        "model_file",
    ]
    name: str = Field(..., description="Library / framework name")
    evidence: list[Evidence] = Field(default_factory=list)


class DecisionSurface(BaseModel):
    """A user-facing endpoint that makes or relays AI decisions."""

    endpoint: str = Field(..., description="Route template, e.g. POST /api/approve")
    file: str
    line: int
    calls_model: bool = False
    has_human_review: bool = False
    has_audit_log: bool = False


class DataSignals(BaseModel):
    pii_fields: list[str] = Field(default_factory=list)
    has_dpia_doc: bool = False
    has_model_card: bool = False
    has_data_card: bool = False
    audit_logging: Literal["none", "partial", "present"] = "none"


class RepoInfo(BaseModel):
    url: str
    ref: str = "main"
    commit: str | None = None
    languages: list[str] = Field(default_factory=list)
    total_files: int = 0
    scanned_files: int = 0


class AISystemProfile(BaseModel):
    """Structured input for compliance agents. Replaces the free-text description."""

    scan_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    repo: RepoInfo
    ai_components: list[AIComponent] = Field(default_factory=list)
    decision_surfaces: list[DecisionSurface] = Field(default_factory=list)
    data_signals: DataSignals = Field(default_factory=DataSignals)
    findings: list[Finding] = Field(default_factory=list)
    stats: dict[str, Any] = Field(default_factory=dict)

    def findings_by_severity(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.findings:
            if f.suppressed:
                continue
            out[f.severity.value] = out.get(f.severity.value, 0) + 1
        return out
