"""Typed query request/response models for the compliance reasoning engine.

4 query types:
  - ComplianceQuery: General compliance question
  - RiskClassification: Classify AI system risk level
  - ObligationLookup: Find obligations for a scenario
  - CrossRegulation: Analyse cross-regulation interactions

6 answer templates:
  prohibition, obligation, conditional_permission,
  non_applicable, legal_uncertainty, general
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


# ── Answer types ──────────────────────────────────────────────────────────────

AnswerType = Literal[
    "prohibition",
    "obligation",
    "conditional_permission",
    "non_applicable",
    "legal_uncertainty",
    "general",
]


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Citation(BaseModel):
    """A reference to a specific legal provision."""
    entity_id: str
    entity_type: str = ""
    regulation_id: str = ""
    article_number: str = ""
    description: str = ""
    relevance_score: float = 0.0


class ReasoningStep(BaseModel):
    """One step in the reasoning chain."""
    step_number: int
    action: str  # e.g., "retrieve", "classify", "apply_rule", "synthesize"
    description: str
    entity_ids: list[str] = Field(default_factory=list)


# ── Compliance Query ──────────────────────────────────────────────────────────

class ComplianceQueryRequest(BaseModel):
    """General compliance question."""
    question: str
    regulation_filter: str | None = None  # "GDPR", "EU_AI_ACT", or None for both
    max_results: int = 10
    include_reasoning: bool = True


class ComplianceQueryResponse(BaseModel):
    """Response to a general compliance question."""
    question: str
    answer: str
    answer_type: AnswerType = "general"
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    citations: list[Citation] = Field(default_factory=list)
    reasoning_chain: list[ReasoningStep] = Field(default_factory=list)
    retrieval_count: int = 0
    raw_results: list[dict[str, Any]] = Field(default_factory=list)


# ── Risk Classification ──────────────────────────────────────────────────────

class RiskClassificationRequest(BaseModel):
    """Classify AI system risk level."""
    system_description: str
    use_case: str | None = None
    sector: str | None = None


class RiskClassificationResponse(BaseModel):
    """Risk classification result."""
    system_description: str
    risk_level: str  # "PROHIBITED", "HIGH_RISK", "LIMITED_RISK", "MINIMAL_RISK"
    matched_categories: list[str] = Field(default_factory=list)
    obligations: list[str] = Field(default_factory=list)
    answer: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    citations: list[Citation] = Field(default_factory=list)
    reasoning_chain: list[ReasoningStep] = Field(default_factory=list)


# ── Obligation Lookup ─────────────────────────────────────────────────────────

class ObligationLookupRequest(BaseModel):
    """Find obligations for a given scenario."""
    scenario: str
    actor_type: str | None = None  # e.g., "controller", "provider"
    regulation_filter: str | None = None


class ObligationLookupResponse(BaseModel):
    """Obligation lookup result."""
    scenario: str
    obligations: list[dict[str, Any]] = Field(default_factory=list)
    exemptions: list[dict[str, Any]] = Field(default_factory=list)
    penalties: list[dict[str, Any]] = Field(default_factory=list)
    answer: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    citations: list[Citation] = Field(default_factory=list)
    reasoning_chain: list[ReasoningStep] = Field(default_factory=list)


# ── Cross-Regulation ─────────────────────────────────────────────────────────

class CrossRegulationRequest(BaseModel):
    """Analyse cross-regulation interactions."""
    topic: str
    gdpr_articles: list[str] = Field(default_factory=list)
    ai_act_articles: list[str] = Field(default_factory=list)


class CrossRegulationResponse(BaseModel):
    """Cross-regulation analysis result."""
    topic: str
    interaction_type: str = ""  # "REINFORCES", "CREATES_EXCEPTION", "CUMULATIVE", etc.
    combined_obligations: list[str] = Field(default_factory=list)
    answer: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    citations: list[Citation] = Field(default_factory=list)
    reasoning_chain: list[ReasoningStep] = Field(default_factory=list)


# ── Answer Templates ─────────────────────────────────────────────────────────

ANSWER_TEMPLATES: dict[AnswerType, str] = {
    "prohibition": (
        "This activity is PROHIBITED. {detail}\n\n"
        "Legal basis: {citations}\n"
        "Penalty: {penalty}"
    ),
    "obligation": (
        "The following obligations apply: {detail}\n\n"
        "Duty bearer: {actor}\n"
        "Legal basis: {citations}\n"
        "Penalty for non-compliance: {penalty}"
    ),
    "conditional_permission": (
        "This is PERMITTED subject to the following conditions: {detail}\n\n"
        "Conditions: {conditions}\n"
        "Legal basis: {citations}"
    ),
    "non_applicable": (
        "The regulation does NOT APPLY in this scenario. {detail}\n\n"
        "Exemption basis: {citations}\n"
        "Scope exclusion: {exclusion}"
    ),
    "legal_uncertainty": (
        "There is LEGAL UNCERTAINTY on this point. {detail}\n\n"
        "Conflicting sources: {conflicts}\n"
        "Recommended approach: {recommendation}"
    ),
    "general": (
        "{detail}\n\n"
        "Relevant provisions: {citations}"
    ),
}
