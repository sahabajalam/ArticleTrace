"""Unit tests for Technical Assessor Agent."""

import pytest
from unittest.mock import AsyncMock, patch

from src.state.compliance_state import (
    create_initial_state,
    ViolationSeverity,
    GDPRViolation,
)


class TestTechnicalAssessor:
    """Tests for Technical Assessor Agent."""

    @pytest.fixture
    def mock_state_with_biometrics(self):
        """Create state for biometric system test."""
        state = create_initial_state(
            system_description="Facial recognition for employee attendance",
            system_type="facial_recognition",
            deployment_context="employment",
        )
        state["risk_classification"] = {
            "category": "HIGH_RISK",
            "annex": "Annex III (4)",
        }
        return state

    def test_gdpr_checklist_defined(self):
        """Test that GDPR checklist is properly defined."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        assert "data_minimization" in agent.GDPR_CHECKLIST
        assert "lawful_basis" in agent.GDPR_CHECKLIST
        assert "special_category_data" in agent.GDPR_CHECKLIST
        assert "automated_decisions" in agent.GDPR_CHECKLIST

    def test_gdpr_checklist_has_articles(self):
        """Test that each GDPR checklist item has article reference."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        for requirement in agent.GDPR_CHECKLIST.values():
            assert "article" in requirement
            assert "Article" in requirement["article"]
            assert "questions" in requirement
            assert len(requirement["questions"]) > 0

    def test_dpia_required_for_special_category(self):
        """Test DPIA requirement for special category data."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        result = agent._is_dpia_required(
            violations=[],
            processes_special_category=True,
            automated_decision_making=False,
            risk_classification={},
        )

        assert result is True

    def test_dpia_required_for_automated_decisions(self):
        """Test DPIA requirement for automated decision-making."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        result = agent._is_dpia_required(
            violations=[],
            processes_special_category=False,
            automated_decision_making=True,
            risk_classification={},
        )

        assert result is True

    def test_dpia_required_for_high_risk(self):
        """Test DPIA requirement for high-risk classification."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        result = agent._is_dpia_required(
            violations=[],
            processes_special_category=False,
            automated_decision_making=False,
            risk_classification={"category": "HIGH_RISK"},
        )

        assert result is True

    def test_dpia_not_required_for_minimal_risk(self):
        """Test DPIA not required for minimal risk systems."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        result = agent._is_dpia_required(
            violations=[],
            processes_special_category=False,
            automated_decision_making=False,
            risk_classification={"category": "MINIMAL_RISK"},
        )

        assert result is False

    def test_recommendations_for_article_9_violation(self):
        """Test recommendations generation for Article 9 violations."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        violations = [
            GDPRViolation(
                article="Article 9",
                issue="Processing biometric data without consent",
                severity=ViolationSeverity.CRITICAL,
            )
        ]

        recommendations = agent._generate_recommendations(
            violations=violations,
            warnings=[],
            risk_classification={},
        )

        assert any("consent" in r.lower() for r in recommendations)

    def test_recommendations_for_article_22_violation(self):
        """Test recommendations generation for Article 22 violations."""
        from src.agents.technical_assessor import TechnicalAssessorAgent

        agent = TechnicalAssessorAgent()

        violations = [
            GDPRViolation(
                article="Article 22",
                issue="Automated decisions without human oversight",
                severity=ViolationSeverity.HIGH,
            )
        ]

        recommendations = agent._generate_recommendations(
            violations=violations,
            warnings=[],
            risk_classification={},
        )

        assert any("human" in r.lower() for r in recommendations)


class TestViolationSeverity:
    """Tests for violation severity classification."""

    def test_severity_levels(self):
        """Test severity level enum values."""
        assert ViolationSeverity.LOW.value == "LOW"
        assert ViolationSeverity.MEDIUM.value == "MEDIUM"
        assert ViolationSeverity.HIGH.value == "HIGH"
        assert ViolationSeverity.CRITICAL.value == "CRITICAL"
