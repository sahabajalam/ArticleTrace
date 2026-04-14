"""SQLAlchemy models for repository scans."""

from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, String, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def _json_safe(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, "model_dump"):
        return _json_safe(obj.model_dump(mode="json"))
    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_json_safe(item) for item in obj]
    return obj


class ScanModel(Base):
    """Persistent record of a repository scan."""

    __tablename__ = "scans"

    scan_id = Column(String(40), primary_key=True)
    repo_url = Column(Text, nullable=False)
    ref = Column(String(100), nullable=False, default="main")

    workflow_status = Column(String(32), nullable=False, default="running")
    current_step = Column(String(64), default="initialized")

    profile = Column(JSON, nullable=True)
    risk_posture = Column(JSON, nullable=True)
    finding_citations = Column(JSON, default=lambda: [])
    narrative = Column(JSON, nullable=True)
    final_report = Column(JSON, nullable=True)

    errors = Column(JSON, default=lambda: [])
    cost_tracking = Column(JSON, default=lambda: {})
    audit_log = Column(JSON, default=lambda: [])

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_state_dict(self) -> dict[str, Any]:
        return {
            "scan_id": self.scan_id,
            "repo_url": self.repo_url,
            "ref": self.ref,
            "profile": self.profile,
            "risk_posture": self.risk_posture,
            "finding_citations": self.finding_citations or [],
            "narrative": self.narrative,
            "final_report": self.final_report,
            "current_step": self.current_step,
            "workflow_status": self.workflow_status,
            "errors": self.errors or [],
            "cost_tracking": self.cost_tracking or {},
            "audit_log": self.audit_log or [],
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "ScanModel":
        started = state.get("started_at")
        completed = state.get("completed_at")
        return cls(
            scan_id=state["scan_id"],
            repo_url=state["repo_url"],
            ref=state.get("ref", "main"),
            profile=_json_safe(state.get("profile")),
            risk_posture=_json_safe(state.get("risk_posture")),
            finding_citations=_json_safe(state.get("finding_citations", [])),
            narrative=_json_safe(state.get("narrative")),
            final_report=_json_safe(state.get("final_report")),
            current_step=state.get("current_step", "initialized"),
            workflow_status=state.get("workflow_status", "running"),
            errors=_json_safe(state.get("errors", [])),
            cost_tracking=_json_safe(state.get("cost_tracking", {})),
            audit_log=_json_safe(state.get("audit_log", [])),
            started_at=datetime.fromisoformat(started) if isinstance(started, str) else datetime.utcnow(),
            completed_at=datetime.fromisoformat(completed) if isinstance(completed, str) else None,
        )

    def update_from_state(self, state: dict[str, Any]) -> None:
        for field in (
            "profile",
            "risk_posture",
            "finding_citations",
            "narrative",
            "final_report",
            "errors",
            "cost_tracking",
            "audit_log",
        ):
            if field in state and state[field] is not None:
                setattr(self, field, _json_safe(state[field]))
        if state.get("current_step"):
            self.current_step = state["current_step"]
        if state.get("workflow_status"):
            self.workflow_status = state["workflow_status"]
        completed = state.get("completed_at")
        if completed:
            self.completed_at = (
                datetime.fromisoformat(completed) if isinstance(completed, str) else completed
            )
        self.updated_at = datetime.utcnow()
