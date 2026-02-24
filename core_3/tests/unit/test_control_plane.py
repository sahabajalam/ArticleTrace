"""Unit tests for Agent Control Plane."""

import pytest
from datetime import datetime

from src.control_plane.governance import (
    AgentControlPlane,
    GovernancePolicy,
    AgentPermissionLevel,
    RateLimiter,
)
from src.control_plane.approval_queue import (
    ApprovalQueue,
    ApprovalRequest,
    ApprovalStatus,
)


class TestGovernancePolicy:
    """Tests for GovernancePolicy."""

    def test_policy_creation(self):
        """Test creating a governance policy."""
        policy = GovernancePolicy(
            agent_name="test_agent",
            max_api_calls_per_hour=50,
            max_spend_per_action_usd=0.10,
            permission_level=AgentPermissionLevel.WRITE_ALLOWED,
            requires_human_approval_if=["classification == PROHIBITED"],
        )

        assert policy.agent_name == "test_agent"
        assert policy.max_api_calls_per_hour == 50
        assert policy.max_spend_per_action_usd == 0.10
        assert policy.permission_level == AgentPermissionLevel.WRITE_ALLOWED

    def test_policy_immutability(self):
        """Test that policies are immutable."""
        policy = GovernancePolicy(
            agent_name="test_agent",
            max_api_calls_per_hour=50,
        )

        with pytest.raises(Exception):
            policy.agent_name = "different_agent"


class TestRateLimiter:
    """Tests for RateLimiter."""

    def test_rate_limiter_allows_first_call(self):
        """Test that first call is allowed."""
        limiter = RateLimiter()
        assert limiter.check("test_agent", max_calls_per_hour=10) is True

    def test_rate_limiter_tracks_calls(self):
        """Test that calls are tracked."""
        limiter = RateLimiter()

        limiter.increment("test_agent")
        remaining = limiter.get_remaining("test_agent", max_calls_per_hour=10)

        assert remaining == 9

    def test_rate_limiter_blocks_excess_calls(self):
        """Test that excess calls are blocked."""
        limiter = RateLimiter()

        # Fill up the limit
        for _ in range(10):
            limiter.increment("test_agent")

        # 11th call should be blocked
        assert limiter.check("test_agent", max_calls_per_hour=10) is False


class TestAgentControlPlane:
    """Tests for AgentControlPlane."""

    def test_default_policies_exist(self):
        """Test that default policies are defined."""
        plane = AgentControlPlane()

        assert "risk_classifier" in plane.policies
        assert "technical_assessor" in plane.policies
        assert "legal_research" in plane.policies
        assert "documentation_generator" in plane.policies

    def test_get_policy(self):
        """Test getting a policy."""
        plane = AgentControlPlane()

        policy = plane.get_policy("risk_classifier")

        assert policy.agent_name == "risk_classifier"
        assert policy.max_api_calls_per_hour > 0

    def test_get_policy_unknown_agent(self):
        """Test getting policy for unknown agent."""
        plane = AgentControlPlane()

        policy = plane.get_policy("unknown_agent")

        assert policy.agent_name == "unknown_agent"  # Returns default policy

    @pytest.mark.asyncio
    async def test_authorize_action_success(self):
        """Test successful authorization."""
        plane = AgentControlPlane()

        result = await plane.authorize_action(
            agent_name="risk_classifier",
            action={"description": "classify risk"},
            cost_estimate=0.05,
        )

        assert result["authorized"] is True

    @pytest.mark.asyncio
    async def test_authorize_action_cost_exceeded(self):
        """Test authorization fails when cost exceeded."""
        plane = AgentControlPlane()

        result = await plane.authorize_action(
            agent_name="risk_classifier",
            action={"description": "classify risk"},
            cost_estimate=100.0,  # Way over limit
        )

        assert result["authorized"] is False
        assert "cost" in result["reason"].lower()

    def test_evaluate_condition_equality(self):
        """Test condition evaluation with equality."""
        plane = AgentControlPlane()

        action = {"classification": "PROHIBITED"}

        assert plane._evaluate_condition("classification == PROHIBITED", action) is True
        assert plane._evaluate_condition("classification == HIGH_RISK", action) is False

    def test_evaluate_condition_comparison(self):
        """Test condition evaluation with comparison."""
        plane = AgentControlPlane()

        action = {"confidence": 0.7}

        assert plane._evaluate_condition("confidence < 0.75", action) is True
        assert plane._evaluate_condition("confidence > 0.8", action) is False

    def test_evaluate_condition_always(self):
        """Test 'always' condition."""
        plane = AgentControlPlane()

        assert plane._evaluate_condition("always", {}) is True

    def test_log_decision(self):
        """Test decision logging."""
        plane = AgentControlPlane()

        plane.log_decision(
            agent_name="test_agent",
            action={"type": "test"},
            outcome={"status": "success", "cost": 0.05},
        )

        assert len(plane.audit_log) == 1
        assert plane.audit_log[0]["agent"] == "test_agent"

    def test_get_statistics(self):
        """Test getting statistics."""
        plane = AgentControlPlane()

        stats = plane.get_statistics()

        assert "total_decisions" in stats
        assert "cost_statistics" in stats
        assert "policies" in stats


class TestApprovalQueue:
    """Tests for ApprovalQueue."""

    def test_approval_request_creation(self):
        """Test creating an approval request."""
        request = ApprovalRequest(
            agent="test_agent",
            action={"type": "test"},
            context={"reason": "testing"},
            risk_level="MEDIUM",
        )

        assert request.agent == "test_agent"
        assert request.status == ApprovalStatus.PENDING
        assert request.id is not None

    @pytest.mark.asyncio
    async def test_request_approval(self):
        """Test requesting approval."""
        queue = ApprovalQueue()

        request = await queue.request_approval(
            agent_name="test_agent",
            action={"classification": "PROHIBITED"},
            context={"reason": "prohibited system detected"},
        )

        assert request.id is not None
        assert request.status == ApprovalStatus.PENDING
        assert request.risk_level == "CRITICAL"  # Should be critical for PROHIBITED

    @pytest.mark.asyncio
    async def test_approve_request(self):
        """Test approving a request."""
        queue = ApprovalQueue()

        request = await queue.request_approval(
            agent_name="test_agent",
            action={"type": "test"},
            context={},
        )

        result = await queue.approve(
            request_id=request.id,
            reviewer_id="human_reviewer",
            notes="Approved for testing",
        )

        assert result.status == ApprovalStatus.APPROVED
        assert result.reviewer_id == "human_reviewer"
        assert result.reviewed_at is not None

    @pytest.mark.asyncio
    async def test_reject_request(self):
        """Test rejecting a request."""
        queue = ApprovalQueue()

        request = await queue.request_approval(
            agent_name="test_agent",
            action={"type": "test"},
            context={},
        )

        result = await queue.reject(
            request_id=request.id,
            reviewer_id="human_reviewer",
            notes="Rejected for testing",
        )

        assert result.status == ApprovalStatus.REJECTED

    def test_get_pending_requests(self):
        """Test getting pending requests."""
        queue = ApprovalQueue()

        # Initially empty
        pending = queue.get_pending_requests()
        assert len(pending) == 0

    def test_get_statistics(self):
        """Test getting statistics."""
        queue = ApprovalQueue()

        stats = queue.get_statistics()

        assert "total_requests" in stats
        assert "by_status" in stats
        assert "pending_count" in stats
