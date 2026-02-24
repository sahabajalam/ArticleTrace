"""Tests for compliance monitoring."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.compliance.eu_ai_act import Article14Monitor, ComplianceResult
from src.compliance.gdpr import GDPRMonitor
from src.database.models import DecisionLog


class TestArticle14Monitor:
    """Test EU AI Act Article 14 compliance monitoring."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return MagicMock()

    @pytest.fixture
    def monitor(self, mock_db):
        """Create monitor instance."""
        return Article14Monitor(mock_db)

    def test_high_risk_without_review_violation(self, monitor):
        """Test HIGH_RISK decision without human review raises violation."""
        decision = DecisionLog(
            id="test-001",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            human_reviewed=False,
            human_override=False,
            input_data={"system": "facial recognition"},
        )

        result = monitor.check_decision(decision)

        assert not result.compliant
        assert len(result.violations) >= 1
        assert any("Human oversight required" in v["rule"] for v in result.violations)

    def test_high_risk_with_review_compliant(self, monitor, mock_db):
        """Test HIGH_RISK decision with human review is compliant."""
        # Mock rate calculations to return 0
        monitor._calculate_human_review_rate = MagicMock(return_value=0.05)
        monitor._calculate_human_override_rate = MagicMock(return_value=0.05)
        monitor._get_days_since_first_decision = MagicMock(return_value=10)

        decision = DecisionLog(
            id="test-002",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            human_reviewed=True,
            human_override=False,
            input_data={"system": "facial recognition"},
        )

        result = monitor.check_decision(decision)

        assert result.compliant

    def test_prohibited_requires_review(self, monitor):
        """Test PROHIBITED decision requires human review."""
        decision = DecisionLog(
            id="test-003",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="PROHIBITED",
            confidence=0.95,
            human_reviewed=False,
        )

        result = monitor.check_decision(decision)

        assert not result.compliant
        assert any("PROHIBITED" in v["message"] for v in result.violations)

    def test_minimal_risk_no_review_required(self, monitor, mock_db):
        """Test MINIMAL_RISK doesn't require review."""
        monitor._calculate_human_review_rate = MagicMock(return_value=0.05)
        monitor._calculate_human_override_rate = MagicMock(return_value=0.05)
        monitor._get_days_since_first_decision = MagicMock(return_value=10)

        decision = DecisionLog(
            id="test-004",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="MINIMAL_RISK",
            confidence=0.88,
            human_reviewed=False,
        )

        result = monitor.check_decision(decision)

        # Should be compliant (no HIGH_RISK violations)
        high_risk_violations = [
            v for v in result.violations if "HIGH_RISK" in v.get("message", "")
        ]
        assert len(high_risk_violations) == 0


class TestGDPRMonitor:
    """Test GDPR Article 22 compliance monitoring."""

    @pytest.fixture
    def mock_db(self):
        """Create mock database session."""
        return MagicMock()

    @pytest.fixture
    def monitor(self, mock_db):
        """Create monitor instance."""
        return GDPRMonitor(mock_db)

    def test_user_not_informed_violation(self, monitor):
        """Test user not informed raises violation."""
        decision = DecisionLog(
            id="test-001",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            metadata={"user_informed": False},
        )

        result = monitor.check_decision(decision)

        assert not result.compliant
        assert any("Transparency" in v["rule"] for v in result.violations)

    def test_no_human_intervention_violation(self, monitor):
        """Test no human intervention raises critical violation."""
        decision = DecisionLog(
            id="test-002",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            metadata={
                "user_informed": True,
                "human_intervention_available": False,
            },
        )

        result = monitor.check_decision(decision)

        assert not result.compliant
        critical = [v for v in result.violations if v["severity"] == "CRITICAL"]
        assert len(critical) >= 1

    def test_special_category_data_without_consent(self, monitor):
        """Test special category data without consent."""
        decision = DecisionLog(
            id="test-003",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            input_data={"biometric_data": "fingerprint"},
            metadata={"user_informed": True},
        )

        result = monitor.check_decision(decision)

        assert not result.compliant
        assert any("Article 9" in v["rule"] for v in result.violations)

    def test_special_category_with_consent_compliant(self, monitor):
        """Test special category data with consent is compliant."""
        decision = DecisionLog(
            id="test-004",
            timestamp=datetime.utcnow(),
            agent_name="risk_classifier",
            prediction="HIGH_RISK",
            confidence=0.92,
            input_data={"biometric_data": "fingerprint"},
            metadata={
                "user_informed": True,
                "explicit_consent": True,
            },
        )

        result = monitor.check_decision(decision)

        # No Article 9 violations
        article9_violations = [
            v for v in result.violations if "Article 9" in v["rule"]
        ]
        assert len(article9_violations) == 0
