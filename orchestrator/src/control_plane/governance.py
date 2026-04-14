"""Agent governance and control plane."""

from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from collections import defaultdict
from threading import Lock

from pydantic import BaseModel, Field

from src.config import settings
from src.utils.logging import get_logger
from src.utils.cost_tracker import cost_tracker

logger = get_logger(__name__)


class AgentPermissionLevel(str, Enum):
    """Permission levels for agents."""

    READ_ONLY = "read"
    WRITE_ALLOWED = "write"
    REQUIRES_APPROVAL = "approval"


class GovernancePolicy(BaseModel):
    """Governance policy for an agent."""

    agent_name: str
    max_api_calls_per_hour: int = Field(default=100)
    max_spend_per_action_usd: float = Field(default=0.50)
    permission_level: AgentPermissionLevel = Field(default=AgentPermissionLevel.WRITE_ALLOWED)
    requires_human_approval_if: list[str] = Field(default_factory=list)

    class Config:
        frozen = True


class RateLimiter:
    """Rate limiter for API calls."""

    def __init__(self):
        self._call_counts: dict[str, list[datetime]] = defaultdict(list)
        self._lock = Lock()

    def check(self, agent_name: str, max_calls_per_hour: int) -> bool:
        """Check if agent can make another call."""
        with self._lock:
            now = datetime.utcnow()
            one_hour_ago = now - timedelta(hours=1)

            # Filter to calls within the last hour
            recent_calls = [
                t for t in self._call_counts[agent_name]
                if t > one_hour_ago
            ]
            self._call_counts[agent_name] = recent_calls

            return len(recent_calls) < max_calls_per_hour

    def increment(self, agent_name: str) -> None:
        """Record a new API call."""
        with self._lock:
            self._call_counts[agent_name].append(datetime.utcnow())

    def get_remaining(self, agent_name: str, max_calls_per_hour: int) -> int:
        """Get remaining calls for the hour."""
        with self._lock:
            now = datetime.utcnow()
            one_hour_ago = now - timedelta(hours=1)
            recent_calls = [
                t for t in self._call_counts[agent_name]
                if t > one_hour_ago
            ]
            return max(0, max_calls_per_hour - len(recent_calls))


class AgentControlPlane:
    """
    Central governance system for all agents.

    The Control Plane is the "HR department for AI workers".
    It enforces policies, tracks costs, and ensures agents don't go rogue.
    """

    # Default policies for each agent
    DEFAULT_POLICIES = {
        "risk_classifier": GovernancePolicy(
            agent_name="risk_classifier",
            max_api_calls_per_hour=50,
            max_spend_per_action_usd=0.10,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=["classification == PROHIBITED"],
        ),
        "technical_assessor": GovernancePolicy(
            agent_name="technical_assessor",
            max_api_calls_per_hour=30,
            max_spend_per_action_usd=0.15,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=["violations_detected > 0"],
        ),
        "legal_research": GovernancePolicy(
            agent_name="legal_research",
            max_api_calls_per_hour=100,
            max_spend_per_action_usd=0.50,
            permission_level=AgentPermissionLevel.READ_ONLY,
            requires_human_approval_if=["confidence < 0.75"],
        ),
        "documentation_generator": GovernancePolicy(
            agent_name="documentation_generator",
            max_api_calls_per_hour=20,
            max_spend_per_action_usd=1.00,
            permission_level=AgentPermissionLevel.REQUIRES_APPROVAL,
            requires_human_approval_if=["always"],
        ),
        "supervisor": GovernancePolicy(
            agent_name="supervisor",
            max_api_calls_per_hour=100,
            max_spend_per_action_usd=0.20,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=[],
        ),
    }

    def __init__(self, policies: dict[str, GovernancePolicy] | None = None):
        self.policies = policies or self.DEFAULT_POLICIES
        self.rate_limiter = RateLimiter()
        self.audit_log: list[dict] = []
        self._lock = Lock()

    def get_policy(self, agent_name: str) -> GovernancePolicy:
        """Get policy for an agent."""
        return self.policies.get(
            agent_name,
            GovernancePolicy(agent_name=agent_name),
        )

    async def authorize_action(
        self,
        agent_name: str,
        action: dict[str, Any],
        cost_estimate: float,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Authorize an agent action.

        Returns:
            {
                "authorized": bool,
                "reason": str,
                "requires_approval": bool
            }
        """
        policy = self.get_policy(agent_name)

        # Check 1: Rate limit
        if not self.rate_limiter.check(agent_name, policy.max_api_calls_per_hour):
            logger.warning(
                "Rate limit exceeded",
                agent=agent_name,
                limit=policy.max_api_calls_per_hour,
            )
            return {
                "authorized": False,
                "reason": f"Rate limit exceeded ({policy.max_api_calls_per_hour}/hour)",
                "requires_approval": False,
            }

        # Check 2: Cost limit
        if cost_estimate > policy.max_spend_per_action_usd:
            logger.warning(
                "Cost limit exceeded",
                agent=agent_name,
                cost_estimate=cost_estimate,
                limit=policy.max_spend_per_action_usd,
            )
            return {
                "authorized": False,
                "reason": f"Cost ${cost_estimate:.2f} exceeds limit ${policy.max_spend_per_action_usd}",
                "requires_approval": True,
            }

        # Check 3: Global daily limit
        can_proceed, reason = cost_tracker.can_proceed(cost_estimate, session_id)
        if not can_proceed:
            return {
                "authorized": False,
                "reason": reason,
                "requires_approval": True,
            }

        # Check 4: Approval conditions
        for condition in policy.requires_human_approval_if:
            if self._evaluate_condition(condition, action):
                logger.info(
                    "Human approval required",
                    agent=agent_name,
                    condition=condition,
                )
                return {
                    "authorized": False,
                    "reason": f"Approval required: {condition}",
                    "requires_approval": True,
                }

        # All checks passed
        self.rate_limiter.increment(agent_name)

        return {"authorized": True, "reason": "OK", "requires_approval": False}

    def _evaluate_condition(self, condition: str, action: dict[str, Any]) -> bool:
        """Evaluate an approval condition against an action."""
        # Simple condition evaluation
        if condition == "always":
            return True

        if "==" in condition:
            key, value = condition.split("==")
            key = key.strip()
            value = value.strip()
            return str(action.get(key, "")).upper() == value.upper()

        if ">" in condition:
            key, value = condition.split(">")
            key = key.strip()
            value = float(value.strip())
            return float(action.get(key, 0)) > value

        if "<" in condition:
            key, value = condition.split("<")
            key = key.strip()
            value = float(value.strip())
            return float(action.get(key, 1)) < value

        return False

    def log_decision(
        self,
        agent_name: str,
        action: dict[str, Any],
        outcome: dict[str, Any],
    ) -> None:
        """Log an agent decision for audit trail."""
        with self._lock:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "agent": agent_name,
                "action": action,
                "outcome": outcome,
                "cost_usd": outcome.get("cost", 0),
                "duration_seconds": outcome.get("duration", 0),
            }
            self.audit_log.append(log_entry)

            logger.info(
                "Decision logged",
                agent=agent_name,
                cost_usd=log_entry["cost_usd"],
            )

    def get_statistics(self) -> dict[str, Any]:
        """Get control plane statistics."""
        return {
            "total_decisions": len(self.audit_log),
            "cost_statistics": cost_tracker.get_statistics(),
            "rate_limits": {
                agent: self.rate_limiter.get_remaining(agent, policy.max_api_calls_per_hour)
                for agent, policy in self.policies.items()
            },
            "policies": {
                name: policy.model_dump()
                for name, policy in self.policies.items()
            },
        }

    def get_audit_log(
        self,
        agent_name: str | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Get audit log entries."""
        with self._lock:
            logs = self.audit_log

            if agent_name:
                logs = [l for l in logs if l["agent"] == agent_name]

            return logs[-limit:]


# Global control plane instance
control_plane = AgentControlPlane()
