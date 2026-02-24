"""Unit tests for Risk Classifier Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.state.compliance_state import create_initial_state, RiskCategory


class TestRiskClassifier:
    """Tests for Risk Classifier Agent."""

    @pytest.fixture
    def mock_state_prohibited(self):
        """Create state for prohibited system test."""
        return create_initial_state(
            system_description="Emotion detection system for monitoring student engagement in online classes. Analyzes webcam feed to detect if students are focused, confused, or distracted.",
            system_type="emotion_recognition",
            deployment_context="education",
        )

    @pytest.fixture
    def mock_state_high_risk(self):
        """Create state for high-risk system test."""
        return create_initial_state(
            system_description="Facial recognition system for employee attendance tracking. Captures facial images and logs entry/exit times.",
            system_type="facial_recognition",
            deployment_context="employee_monitoring",
        )

    @pytest.fixture
    def mock_state_limited_risk(self):
        """Create state for limited-risk system test."""
        return create_initial_state(
            system_description="AI-powered chatbot for customer service. Clearly disclosed as AI at start of conversation.",
            system_type="chatbot",
            deployment_context="customer_service",
        )

    @pytest.fixture
    def mock_state_minimal_risk(self):
        """Create state for minimal-risk system test."""
        return create_initial_state(
            system_description="Machine learning model that filters spam emails from inbox.",
            system_type="spam_filter",
            deployment_context="email_service",
        )

    def test_prohibited_patterns_defined(self):
        """Test that prohibited patterns are properly defined."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        assert len(agent.PROHIBITED_PATTERNS) > 0
        assert "emotion recognition in workplace" in agent.PROHIBITED_PATTERNS
        assert "emotion recognition in education" in agent.PROHIBITED_PATTERNS
        assert "social scoring by public authorities" in agent.PROHIBITED_PATTERNS

    def test_high_risk_categories_defined(self):
        """Test that high-risk categories are properly defined."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        assert "employment" in agent.HIGH_RISK_CATEGORIES
        assert "education" in agent.HIGH_RISK_CATEGORIES
        assert "essential_services" in agent.HIGH_RISK_CATEGORIES
        assert "biometric_identification" in agent.HIGH_RISK_CATEGORIES

    def test_check_prohibited_emotion_education(self):
        """Test detection of prohibited emotion recognition in education."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        capabilities = {
            "primary_function": "emotion detection for student engagement",
            "data_types": ["biometric", "behavioral"],
            "decision_impact": "student assessment",
            "deployment_context": "education",
            "involves_emotions": True,
            "keywords": ["emotion", "student", "engagement"],
        }

        result = agent._check_prohibited(capabilities)

        assert result["is_prohibited"] is True
        assert "Article 5" in result["reason"]
        assert result["confidence"] >= 0.9

    def test_check_prohibited_emotion_workplace(self):
        """Test detection of prohibited emotion recognition in workplace."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        capabilities = {
            "primary_function": "workplace satisfaction monitoring",
            "data_types": ["biometric", "behavioral"],
            "decision_impact": "employee evaluation",
            "deployment_context": "workplace",
            "involves_emotions": True,
            "keywords": ["emotion", "workplace", "satisfaction"],
        }

        result = agent._check_prohibited(capabilities)

        assert result["is_prohibited"] is True

    def test_check_high_risk_employment(self):
        """Test detection of high-risk employment systems."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        capabilities = {
            "primary_function": "facial recognition for attendance",
            "data_types": ["biometric"],
            "decision_impact": "employee attendance",
            "deployment_context": "employment",
            "involves_biometrics": True,
            "keywords": ["facial_recognition", "attendance", "employee"],
        }

        result = agent._check_high_risk(capabilities)

        assert result["is_high_risk"] is True
        assert "Annex III" in result["annex"]

    def test_check_high_risk_credit_scoring(self):
        """Test detection of high-risk credit scoring systems."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        capabilities = {
            "primary_function": "credit scoring for loan approval",
            "data_types": ["financial", "personal"],
            "decision_impact": "credit decision",
            "deployment_context": "financial_services",
            "keywords": ["credit_scoring", "loan"],
        }

        result = agent._check_high_risk(capabilities)

        assert result["is_high_risk"] is True
        assert "essential_services" in result["subcategory"]

    def test_is_user_facing(self):
        """Test detection of user-facing systems."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        # User-facing chatbot
        capabilities = {
            "primary_function": "customer service chatbot",
            "keywords": ["chatbot"],
        }
        assert agent._is_user_facing(capabilities, "customer_service") is True

        # Non-user-facing backend
        capabilities = {
            "primary_function": "data processing pipeline",
            "keywords": ["processing"],
        }
        assert agent._is_user_facing(capabilities, "backend") is False

    def test_risk_category_enum_values(self):
        """Test risk category enum values."""
        assert RiskCategory.PROHIBITED.value == "PROHIBITED"
        assert RiskCategory.HIGH_RISK.value == "HIGH_RISK"
        assert RiskCategory.LIMITED_RISK.value == "LIMITED_RISK"
        assert RiskCategory.MINIMAL_RISK.value == "MINIMAL_RISK"


class TestRiskClassifierEdgeCases:
    """Edge case tests for Risk Classifier."""

    def test_empty_capabilities(self):
        """Test handling of empty capabilities."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        capabilities = {
            "primary_function": "",
            "data_types": [],
            "decision_impact": "",
            "deployment_context": "",
            "keywords": [],
        }

        # Should not crash
        prohibited = agent._check_prohibited(capabilities)
        assert prohibited["is_prohibited"] is False

        high_risk = agent._check_high_risk(capabilities)
        assert high_risk["is_high_risk"] is False

    def test_borderline_confidence(self):
        """Test borderline confidence cases."""
        from src.agents.risk_classifier import RiskClassifierAgent

        agent = RiskClassifierAgent()

        # Borderline case - mentions biometrics but unclear context
        capabilities = {
            "primary_function": "identity verification",
            "data_types": ["biometric"],
            "deployment_context": "unknown",
            "involves_biometrics": True,
            "keywords": ["verification"],
        }

        high_risk = agent._check_high_risk(capabilities)
        # Should still detect as high-risk due to biometrics
        # but may have lower confidence
