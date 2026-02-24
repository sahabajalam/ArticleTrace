"""SQLAlchemy models for compliance assessments."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Float, String, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def _make_json_safe(obj: Any) -> Any:
    """Recursively convert datetime and Pydantic objects to JSON-serializable types."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, "model_dump"):
        return _make_json_safe(obj.model_dump())
    if isinstance(obj, dict):
        return {k: _make_json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_json_safe(item) for item in obj]
    return obj


class AssessmentModel(Base):
    """SQLAlchemy model for compliance assessments."""

    __tablename__ = "assessments"

    session_id = Column(String(36), primary_key=True)

    # Input fields
    system_description = Column(Text, nullable=False)
    system_type = Column(String(100), nullable=False)
    deployment_context = Column(String(100), nullable=False)
    company_name = Column(String(255), nullable=True)
    additional_context = Column(JSON, nullable=True)

    # Agent outputs (stored as JSON)
    risk_classification = Column(JSON, nullable=True)
    gdpr_audit = Column(JSON, nullable=True)
    legal_citations = Column(JSON, nullable=True)
    compliance_docs = Column(JSON, nullable=True)
    final_report = Column(JSON, nullable=True)

    # Control flow
    current_step = Column(String(50), default="initialized")
    requires_human_review = Column(String(5), default="false")
    human_decision = Column(String(50), nullable=True)
    workflow_status = Column(String(50), default="running")

    # Error handling
    errors = Column(JSON, default=lambda: [])

    # Metadata
    confidence_scores = Column(JSON, default=lambda: {})
    cost_tracking = Column(JSON, default=lambda: {})
    audit_log = Column(JSON, default=lambda: [])

    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_state_dict(self) -> dict[str, Any]:
        """Convert model to ComplianceState dict format."""
        return {
            "session_id": self.session_id,
            "system_description": self.system_description,
            "system_type": self.system_type,
            "deployment_context": self.deployment_context,
            "company_name": self.company_name,
            "additional_context": self.additional_context,
            "risk_classification": self.risk_classification,
            "gdpr_audit": self.gdpr_audit,
            "legal_citations": self.legal_citations,
            "compliance_docs": self.compliance_docs,
            "final_report": self.final_report,
            "current_step": self.current_step,
            "requires_human_review": self.requires_human_review == "true",
            "human_decision": self.human_decision,
            "workflow_status": self.workflow_status,
            "errors": self.errors or [],
            "confidence_scores": self.confidence_scores or {},
            "cost_tracking": self.cost_tracking or {},
            "audit_log": self.audit_log or [],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "AssessmentModel":
        """Create model from ComplianceState dict."""
        return cls(
            session_id=state["session_id"],
            system_description=state["system_description"],
            system_type=state["system_type"],
            deployment_context=state["deployment_context"],
            company_name=state.get("company_name"),
            additional_context=state.get("additional_context"),
            risk_classification=state.get("risk_classification"),
            gdpr_audit=state.get("gdpr_audit"),
            legal_citations=state.get("legal_citations"),
            compliance_docs=state.get("compliance_docs"),
            final_report=state.get("final_report"),
            current_step=state.get("current_step", "initialized"),
            requires_human_review="true" if state.get("requires_human_review") else "false",
            human_decision=state.get("human_decision"),
            workflow_status=state.get("workflow_status", "running"),
            errors=state.get("errors", []),
            confidence_scores=state.get("confidence_scores", {}),
            cost_tracking=state.get("cost_tracking", {}),
            audit_log=state.get("audit_log", []),
            started_at=datetime.fromisoformat(state["started_at"]) if isinstance(state.get("started_at"), str) else datetime.utcnow(),
            completed_at=datetime.fromisoformat(state["completed_at"]) if state.get("completed_at") else None,
        )

    def update_from_state(self, state: dict[str, Any]) -> None:
        """Update model fields from state dict."""
        if state.get("risk_classification") is not None:
            self.risk_classification = _make_json_safe(state["risk_classification"])
        if state.get("gdpr_audit") is not None:
            self.gdpr_audit = _make_json_safe(state["gdpr_audit"])
        if state.get("legal_citations") is not None:
            self.legal_citations = _make_json_safe(state["legal_citations"])
        if state.get("compliance_docs") is not None:
            self.compliance_docs = _make_json_safe(state["compliance_docs"])
        if state.get("final_report") is not None:
            self.final_report = _make_json_safe(state["final_report"])
        if state.get("current_step"):
            self.current_step = state["current_step"]
        if "requires_human_review" in state:
            self.requires_human_review = "true" if state["requires_human_review"] else "false"
        if state.get("human_decision"):
            self.human_decision = state["human_decision"]
        if state.get("workflow_status"):
            self.workflow_status = state["workflow_status"]
        if state.get("errors") is not None:
            self.errors = _make_json_safe(state["errors"])
        if state.get("confidence_scores") is not None:
            self.confidence_scores = _make_json_safe(state["confidence_scores"])
        if state.get("cost_tracking") is not None:
            self.cost_tracking = _make_json_safe(state["cost_tracking"])
        if state.get("audit_log") is not None:
            self.audit_log = _make_json_safe(state["audit_log"])
        if state.get("completed_at"):
            completed = state["completed_at"]
            self.completed_at = datetime.fromisoformat(completed) if isinstance(completed, str) else completed
        self.updated_at = datetime.utcnow()
