"""Scan-centric LangGraph state.

Flow:
  profile -> risk_posture -> legal_citations -> narrative -> final_report
"""

from __future__ import annotations

import operator
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal, TypedDict

from pydantic import BaseModel, Field

from src.code_analyzer.models import AISystemProfile


def merge_dicts(left: dict, right: dict) -> dict:
    merged = {**left}
    for k, v in right.items():
        if k in merged and isinstance(merged[k], (int, float)) and isinstance(v, (int, float)):
            merged[k] = merged[k] + v
        else:
            merged[k] = v
    return merged


class RiskCategory(str, Enum):
    PROHIBITED = "PROHIBITED"
    HIGH_RISK = "HIGH_RISK"
    LIMITED_RISK = "LIMITED_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"


class RiskPosture(BaseModel):
    """Deterministic risk aggregation over findings."""

    category: RiskCategory
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    prohibited_triggers: list[str] = Field(
        default_factory=list,
        description="Rule IDs that triggered PROHIBITED classification",
    )
    reason: str
    compliance_score: float = Field(..., ge=0.0, le=100.0)


class LegalCitation(BaseModel):
    regulation: str
    article_number: str
    title: str | None = None
    text_snippet: str | None = None
    relevance_score: float = 0.0
    obligation_anchor: str | None = None


class FindingCitations(BaseModel):
    """Citations attached to a specific finding."""

    rule_id: str
    citations: list[LegalCitation] = Field(default_factory=list)
    reasoning_chain: list[str] = Field(default_factory=list)


class RemediationStep(BaseModel):
    priority: Literal["immediate", "short_term", "long_term"]
    finding_rule_ids: list[str]
    title: str
    description: str
    effort: Literal["low", "medium", "high"] = "medium"


class NarrativeReport(BaseModel):
    executive_summary: str
    risk_narrative: str
    top_findings_narrative: str
    remediation_plan: list[RemediationStep] = Field(default_factory=list)


class ScanReport(BaseModel):
    """The final artefact a scan produces."""

    scan_id: str
    repo_url: str
    ref: str
    risk_posture: RiskPosture
    profile: AISystemProfile
    finding_citations: list[FindingCitations] = Field(default_factory=list)
    narrative: NarrativeReport | None = None
    completed_at: str
    cost_tracking: dict[str, float] = Field(default_factory=dict)


class ScanState(TypedDict):
    """LangGraph state for a scan workflow."""

    scan_id: str
    repo_url: str
    ref: str

    profile: dict  # AISystemProfile as dict (LangGraph serializes TypedDict values)
    risk_posture: dict | None
    finding_citations: list[dict]
    narrative: dict | None
    final_report: dict | None

    current_step: str
    workflow_status: Literal["running", "completed", "failed"]

    errors: Annotated[list[str], operator.add]
    cost_tracking: Annotated[dict[str, float], merge_dicts]
    audit_log: Annotated[list[dict], operator.add]

    started_at: str
    completed_at: str | None


def create_initial_state(
    scan_id: str,
    repo_url: str,
    ref: str,
    profile: AISystemProfile,
) -> ScanState:
    return ScanState(
        scan_id=scan_id,
        repo_url=repo_url,
        ref=ref,
        profile=profile.model_dump(mode="json"),
        risk_posture=None,
        finding_citations=[],
        narrative=None,
        final_report=None,
        current_step="initialized",
        workflow_status="running",
        errors=[],
        cost_tracking={},
        audit_log=[],
        started_at=datetime.utcnow().isoformat(),
        completed_at=None,
    )
