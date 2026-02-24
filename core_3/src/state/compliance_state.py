"""Compliance state definitions for multi-agent workflow."""

import operator
from typing import Annotated, TypedDict, Literal, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


def merge_dicts(left: dict, right: dict) -> dict:
    """Reducer that merges two dicts (right overwrites left on key conflicts)."""
    merged = {**left}
    for k, v in right.items():
        if k in merged and isinstance(merged[k], (int, float)) and isinstance(v, (int, float)):
            merged[k] = merged[k] + v
        else:
            merged[k] = v
    return merged


class RiskCategory(str, Enum):
    """EU AI Act risk classification categories."""

    PROHIBITED = "PROHIBITED"
    HIGH_RISK = "HIGH_RISK"
    LIMITED_RISK = "LIMITED_RISK"
    MINIMAL_RISK = "MINIMAL_RISK"


class ViolationSeverity(str, Enum):
    """Severity levels for compliance violations."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskClassification(BaseModel):
    """Output from Risk Classifier Agent."""

    category: RiskCategory = Field(..., description="EU AI Act risk category")
    article: str | None = Field(None, description="Relevant EU AI Act article")
    annex: str | None = Field(None, description="Relevant EU AI Act annex")
    subcategory: str | None = Field(None, description="High-risk subcategory if applicable")
    reason: str = Field(..., description="Explanation for classification")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    requirements: list[str] = Field(default_factory=list, description="Required actions")
    action: str | None = Field(None, description="Recommended action")


class GDPRViolation(BaseModel):
    """Individual GDPR violation found during audit."""

    article: str = Field(..., description="GDPR article violated")
    issue: str = Field(..., description="Description of the violation")
    severity: ViolationSeverity = Field(..., description="Violation severity")
    evidence: str | None = Field(None, description="Evidence from system description")


class GDPRWarning(BaseModel):
    """GDPR compliance warning (not a violation)."""

    article: str = Field(..., description="Relevant GDPR article")
    issue: str = Field(..., description="Description of the warning")
    severity: ViolationSeverity = Field(default=ViolationSeverity.MEDIUM)


class GDPRAuditResult(BaseModel):
    """Output from Technical Assessor Agent (GDPR audit)."""

    gdpr_compliant: bool = Field(..., description="Overall GDPR compliance status")
    violations: list[GDPRViolation] = Field(default_factory=list)
    warnings: list[GDPRWarning] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    lawful_basis: str | None = Field(None, description="Identified lawful basis for processing")
    special_category_data: bool = Field(
        default=False, description="Whether special category data is processed"
    )
    automated_decision_making: bool = Field(
        default=False, description="Whether Article 22 applies"
    )


class LegalCitation(BaseModel):
    """Legal citation from GraphRAG."""

    regulation: str = Field(..., description="GDPR or EU_AI_ACT")
    article_number: str = Field(..., description="Article/Annex number")
    title: str | None = Field(None, description="Article title")
    text_snippet: str | None = Field(None, description="Relevant text excerpt")
    relevance_score: float = Field(default=0.0, description="Relevance to query")
    relationship: str | None = Field(None, description="Graph relationship type")


class LegalResearchResult(BaseModel):
    """Output from Legal Research Agent."""

    relevant_articles: list[LegalCitation] = Field(default_factory=list)
    relationship_chains: list[list[str]] = Field(
        default_factory=list, description="Multi-hop reasoning chains"
    )
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    query_used: str = Field(default="", description="Query sent to GraphRAG")


class ComplianceDocument(BaseModel):
    """Generated compliance document."""

    doc_type: str = Field(..., description="DPIA, ROPA, CONFORMITY_ASSESSMENT, etc.")
    content: str = Field(..., description="Markdown content of document")
    filename: str = Field(..., description="Suggested filename")
    format: str = Field(default="markdown")
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class DocumentGenerationResult(BaseModel):
    """Output from Documentation Generator Agent."""

    documents: list[ComplianceDocument] = Field(default_factory=list)
    required_docs: list[str] = Field(default_factory=list)


class AgentOutput(BaseModel):
    """Wrapper for any agent output with metadata."""

    agent_name: str = Field(..., description="Name of the agent")
    output: dict[str, Any] = Field(..., description="Agent output data")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    cost_usd: float = Field(default=0.0, ge=0.0)
    duration_seconds: float = Field(default=0.0, ge=0.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AuditLogEntry(BaseModel):
    """Entry in the audit log."""

    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent: str
    action: str
    input_summary: str | None = None
    output_summary: str | None = None
    cost_usd: float = 0.0
    duration_seconds: float = 0.0
    human_approved: bool | None = None


class ComplianceState(TypedDict):
    """
    Shared state across all compliance agents.

    This is the LangGraph state that flows through the workflow.

    Fields with Annotated reducers:
    - errors: appends new errors to existing list
    - audit_log: appends new entries to existing list
    - confidence_scores: merges new scores (additive for numeric values)
    - cost_tracking: merges new costs (additive for numeric values)
    """

    # Input (from user)
    system_description: str
    system_type: str  # e.g., "facial_recognition", "chatbot", "credit_scoring"
    deployment_context: str  # e.g., "employee_monitoring", "customer_service"
    company_name: str | None
    additional_context: dict[str, Any] | None

    # Agent Outputs
    risk_classification: dict | None  # From Risk Classifier Agent
    gdpr_audit: dict | None  # From Technical Assessor Agent
    legal_citations: dict | None  # From Legal Research Agent
    compliance_docs: dict | None  # From Documentation Generator Agent
    final_report: dict | None  # From Supervisor synthesis step

    # Control Flow
    current_step: str
    requires_human_review: bool
    human_decision: str | None
    workflow_status: Literal["running", "awaiting_approval", "completed", "failed"]

    # Error Handling — reducer appends new errors
    errors: Annotated[list[str], operator.add]

    # Metadata — reducers merge/append
    confidence_scores: Annotated[dict[str, float], merge_dicts]
    cost_tracking: Annotated[dict[str, float], merge_dicts]
    audit_log: Annotated[list[dict], operator.add]

    # Session
    session_id: str
    started_at: str
    completed_at: str | None


def create_initial_state(
    system_description: str,
    system_type: str,
    deployment_context: str,
    company_name: str | None = None,
    session_id: str | None = None,
) -> ComplianceState:
    """Create initial compliance state for a new assessment."""
    import uuid

    return ComplianceState(
        # Input
        system_description=system_description,
        system_type=system_type,
        deployment_context=deployment_context,
        company_name=company_name,
        additional_context=None,
        # Agent Outputs
        risk_classification=None,
        gdpr_audit=None,
        legal_citations=None,
        compliance_docs=None,
        final_report=None,
        # Control Flow
        current_step="initialized",
        requires_human_review=False,
        human_decision=None,
        workflow_status="running",
        # Errors
        errors=[],
        # Metadata
        confidence_scores={},
        cost_tracking={},
        audit_log=[],
        # Session
        session_id=session_id or str(uuid.uuid4()),
        started_at=datetime.utcnow().isoformat(),
        completed_at=None,
    )
