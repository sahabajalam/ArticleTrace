"""Human-in-the-loop approval queue."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4
from collections import defaultdict
from threading import Lock

from pydantic import BaseModel, Field

from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class ApprovalStatus(str, Enum):
    """Status of an approval request."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(BaseModel):
    """An approval request awaiting human review."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    agent: str
    action: dict[str, Any]
    context: dict[str, Any] = Field(default_factory=dict)
    risk_level: str = "MEDIUM"
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    reviewed_at: datetime | None = None
    reviewer_id: str | None = None
    reviewer_notes: str | None = None


class ApprovalQueue:
    """
    Manages high-stakes decisions awaiting human review.

    When an agent needs human approval (e.g., for prohibited system
    classification), the request is added to this queue.
    """

    def __init__(self, timeout_hours: int = 24):
        self.timeout_hours = timeout_hours
        self._queue: dict[str, ApprovalRequest] = {}
        self._by_session: dict[str, list[str]] = defaultdict(list)
        self._lock = Lock()

    async def request_approval(
        self,
        agent_name: str,
        action: dict[str, Any],
        context: dict[str, Any],
        session_id: str | None = None,
    ) -> ApprovalRequest:
        """
        Create an approval request.

        Args:
            agent_name: Name of the requesting agent
            action: The action requiring approval
            context: Additional context for reviewer
            session_id: Optional session ID for tracking

        Returns:
            ApprovalRequest object
        """
        risk_level = self._assess_risk_level(action)

        request = ApprovalRequest(
            agent=agent_name,
            action=action,
            context=context,
            risk_level=risk_level,
            expires_at=datetime.utcnow() + timedelta(hours=self.timeout_hours),
        )

        with self._lock:
            self._queue[request.id] = request
            if session_id:
                self._by_session[session_id].append(request.id)

        logger.info(
            "Approval request created",
            request_id=request.id,
            agent=agent_name,
            risk_level=risk_level,
        )

        # In production, would send notification here
        await self._send_notification(request)

        return request

    def _assess_risk_level(self, action: dict[str, Any]) -> str:
        """Assess risk level of an action."""
        # Check for prohibited classification
        if action.get("classification") == "PROHIBITED":
            return "CRITICAL"

        # Check for GDPR violations
        if action.get("violations_detected", 0) > 0:
            return "HIGH"

        # Check confidence
        confidence = action.get("confidence", 1.0)
        if confidence < 0.7:
            return "HIGH"
        elif confidence < 0.85:
            return "MEDIUM"

        return "LOW"

    async def _send_notification(self, request: ApprovalRequest) -> None:
        """Send notification about approval request."""
        # In production, this would send to Slack, email, etc.
        logger.info(
            "Notification sent for approval request",
            request_id=request.id,
            risk_level=request.risk_level,
        )

        # Slack message template (for future implementation)
        slack_message = f"""
:warning: **Agent Approval Required**

**Agent**: {request.agent}
**Risk Level**: {request.risk_level}

**Action**: {request.action.get('description', 'No description')}
**Reasoning**: {request.context.get('agent_reasoning', 'N/A')}
**Confidence**: {request.context.get('confidence_score', 'N/A')}

:white_check_mark: Approve | :x: Reject | :speech_balloon: Request More Info
"""
        # Would call Slack API here if configured

    async def approve(
        self,
        request_id: str,
        reviewer_id: str,
        notes: str | None = None,
    ) -> ApprovalRequest | None:
        """Approve a request."""
        with self._lock:
            request = self._queue.get(request_id)
            if not request:
                return None

            request.status = ApprovalStatus.APPROVED
            request.reviewed_at = datetime.utcnow()
            request.reviewer_id = reviewer_id
            request.reviewer_notes = notes

            logger.info(
                "Approval granted",
                request_id=request_id,
                reviewer_id=reviewer_id,
            )

            return request

    async def reject(
        self,
        request_id: str,
        reviewer_id: str,
        notes: str | None = None,
    ) -> ApprovalRequest | None:
        """Reject a request."""
        with self._lock:
            request = self._queue.get(request_id)
            if not request:
                return None

            request.status = ApprovalStatus.REJECTED
            request.reviewed_at = datetime.utcnow()
            request.reviewer_id = reviewer_id
            request.reviewer_notes = notes

            logger.info(
                "Approval rejected",
                request_id=request_id,
                reviewer_id=reviewer_id,
            )

            return request

    def get_request(self, request_id: str) -> ApprovalRequest | None:
        """Get a specific approval request."""
        return self._queue.get(request_id)

    def get_pending_requests(self, agent_name: str | None = None) -> list[ApprovalRequest]:
        """Get all pending approval requests."""
        with self._lock:
            pending = [
                r for r in self._queue.values()
                if r.status == ApprovalStatus.PENDING
            ]

            if agent_name:
                pending = [r for r in pending if r.agent == agent_name]

            return pending

    def get_session_requests(self, session_id: str) -> list[ApprovalRequest]:
        """Get all requests for a session."""
        request_ids = self._by_session.get(session_id, [])
        return [
            self._queue[rid] for rid in request_ids
            if rid in self._queue
        ]

    async def wait_for_decision(
        self,
        request_id: str,
        timeout_seconds: int = 3600,
    ) -> ApprovalRequest | None:
        """
        Wait for a decision on an approval request.

        In production, this would use async waiting.
        For demo, returns immediately with auto-approval.
        """
        request = self.get_request(request_id)
        if not request:
            return None

        # For demo purposes, auto-approve after a simulated wait
        if request.status == ApprovalStatus.PENDING:
            logger.info(
                "Auto-approving request for demo",
                request_id=request_id,
            )
            return await self.approve(
                request_id,
                reviewer_id="auto_approval_system",
                notes="Auto-approved for demonstration purposes",
            )

        return request

    def cleanup_expired(self) -> int:
        """Clean up expired requests."""
        now = datetime.utcnow()
        expired_count = 0

        with self._lock:
            for request in self._queue.values():
                if (
                    request.status == ApprovalStatus.PENDING
                    and request.expires_at
                    and request.expires_at < now
                ):
                    request.status = ApprovalStatus.EXPIRED
                    expired_count += 1

        if expired_count:
            logger.info(f"Cleaned up {expired_count} expired approval requests")

        return expired_count

    def get_statistics(self) -> dict[str, Any]:
        """Get approval queue statistics."""
        with self._lock:
            total = len(self._queue)
            by_status = defaultdict(int)
            by_risk = defaultdict(int)

            for request in self._queue.values():
                by_status[request.status.value] += 1
                by_risk[request.risk_level] += 1

            return {
                "total_requests": total,
                "by_status": dict(by_status),
                "by_risk_level": dict(by_risk),
                "pending_count": by_status.get("pending", 0),
            }


# Global approval queue instance
approval_queue = ApprovalQueue()
