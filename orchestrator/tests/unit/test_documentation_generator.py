"""Unit tests for Documentation Generator Agent."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.state.compliance_state import create_initial_state, RiskCategory


class TestDocumentationGeneratorAgent:
    """Tests for Documentation Generator Agent."""

    @pytest.fixture
    def mock_state_high_risk(self):
        """Create state for high-risk system test."""
        state = create_initial_state(
            system_description="AI-powered recruitment system that automatically screens resumes and ranks candidates based on qualifications, experience, and predicted job performance.",
            system_type="recruitment_screening",
            deployment_context="employment",
            company_name="TechCorp Inc.",
        )
        state["risk_classification"] = {
            "category": "HIGH_RISK",
            "article": "Article 6",
            "annex": "Annex III",
            "subcategory": "employment",
            "reason": "Employment decision-making AI requires conformity assessment",
            "confidence": 0.95,
            "requirements": ["DPIA", "Conformity Assessment", "Human Oversight"],
        }
        state["gdpr_audit"] = {
            "gdpr_compliant": False,
            "dpia_required": True,
            "special_category_data": False,
            "automated_decision_making": True,
            "violations": [
                {
                    "article": "Article 22",
                    "issue": "Automated decision with legal effects requires explicit consent",
                    "severity": "HIGH",
                }
            ],
            "recommendations": ["Implement human review for final decisions"],
        }
        return state

    @pytest.fixture
    def mock_state_limited_risk(self):
        """Create state for limited-risk system test."""
        state = create_initial_state(
            system_description="Customer service chatbot that answers FAQs and helps with basic account inquiries. Clearly disclosed as AI.",
            system_type="chatbot",
            deployment_context="customer_service",
            company_name="ServiceCo",
        )
        state["risk_classification"] = {
            "category": "LIMITED_RISK",
            "article": "Article 52",
            "reason": "User-facing AI requires transparency notice",
            "confidence": 0.88,
            "requirements": ["Transparency Notice"],
        }
        state["gdpr_audit"] = {
            "gdpr_compliant": True,
            "dpia_required": False,
            "special_category_data": False,
            "automated_decision_making": False,
            "violations": [],
            "recommendations": [],
        }
        return state

    def test_document_types_defined(self):
        """Test that all document types are properly defined."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        assert "DPIA" in agent.DOCUMENT_TYPES
        assert "ROPA" in agent.DOCUMENT_TYPES
        assert "CONFORMITY_ASSESSMENT" in agent.DOCUMENT_TYPES
        assert "TRANSPARENCY_NOTICE" in agent.DOCUMENT_TYPES

    def test_dpia_document_info(self):
        """Test DPIA document type configuration."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()
        dpia_info = agent.DOCUMENT_TYPES["DPIA"]

        assert dpia_info["full_name"] == "Data Protection Impact Assessment"
        assert dpia_info["source"] == "GDPR Article 35"
        assert "high_risk" in dpia_info["required_when"]

    def test_conformity_assessment_info(self):
        """Test Conformity Assessment document type configuration."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()
        ca_info = agent.DOCUMENT_TYPES["CONFORMITY_ASSESSMENT"]

        assert ca_info["full_name"] == "EU AI Act Conformity Assessment"
        assert ca_info["source"] == "EU AI Act Article 43"
        assert "high_risk" in ca_info["required_when"]

    def test_determine_requirements_high_risk(self, mock_state_high_risk):
        """Test document requirements for high-risk system."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        risk_classification = mock_state_high_risk["risk_classification"]
        gdpr_audit = mock_state_high_risk["gdpr_audit"]

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "DPIA" in required
        assert "ROPA" in required
        assert "CONFORMITY_ASSESSMENT" in required

    def test_determine_requirements_limited_risk(self, mock_state_limited_risk):
        """Test document requirements for limited-risk system."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        risk_classification = mock_state_limited_risk["risk_classification"]
        gdpr_audit = mock_state_limited_risk["gdpr_audit"]

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "ROPA" in required
        assert "TRANSPARENCY_NOTICE" in required
        assert "CONFORMITY_ASSESSMENT" not in required

    def test_determine_requirements_special_category_data(self):
        """Test DPIA required when special category data is processed."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        risk_classification = {"category": "MINIMAL_RISK"}
        gdpr_audit = {"special_category_data": True}

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "DPIA" in required

    def test_determine_requirements_dpia_explicit(self):
        """Test DPIA required when explicitly flagged."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        risk_classification = {"category": "MINIMAL_RISK"}
        gdpr_audit = {"dpia_required": True}

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "DPIA" in required

    def test_ropa_always_included(self):
        """Test ROPA is always included in requirements."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        # Even minimal risk systems need ROPA
        risk_classification = {"category": "MINIMAL_RISK"}
        gdpr_audit = {"special_category_data": False, "dpia_required": False}

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "ROPA" in required

    def test_prohibited_system_gets_dpia(self):
        """Test prohibited systems also require DPIA."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        risk_classification = {"category": "PROHIBITED"}
        gdpr_audit = {}

        required = agent._determine_requirements(risk_classification, gdpr_audit)

        assert "DPIA" in required

    @pytest.mark.asyncio
    async def test_execute_generates_documents(self, mock_state_high_risk):
        """Test that execute generates required documents."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        # Mock LLM invocation
        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ("# Generated Document\n\nContent here...", 0.01)

            result = await agent.execute(mock_state_high_risk)

            assert "compliance_docs" in result
            docs = result["compliance_docs"]
            assert docs["generated_count"] > 0
            assert len(docs["documents"]) > 0

    @pytest.mark.asyncio
    async def test_execute_sets_confidence(self, mock_state_limited_risk):
        """Test that execute sets confidence score."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ("# Transparency Notice\n\nContent...", 0.005)

            result = await agent.execute(mock_state_limited_risk)

            assert "confidence_scores" in result
            assert "documentation_generator" in result["confidence_scores"]
            assert result["confidence_scores"]["documentation_generator"] >= 0.0

    @pytest.mark.asyncio
    async def test_execute_updates_current_step(self, mock_state_high_risk):
        """Test that execute updates current step."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ("# Document\n\nContent...", 0.01)

            result = await agent.execute(mock_state_high_risk)

            assert result["current_step"] == "documentation_generated"


class TestDocumentGeneration:
    """Tests for individual document generation methods."""

    @pytest.fixture
    def agent(self):
        """Create agent instance."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent
        return DocumentationGeneratorAgent()

    @pytest.fixture
    def sample_state(self):
        """Create sample state for document generation."""
        state = create_initial_state(
            system_description="AI system for automated credit scoring and loan approval decisions.",
            system_type="credit_scoring",
            deployment_context="financial_services",
            company_name="FinanceAI Corp",
        )
        state["risk_classification"] = {
            "category": "HIGH_RISK",
            "annex": "Annex III",
            "subcategory": "essential_services",
            "requirements": ["Risk management", "Data governance", "Human oversight"],
        }
        state["gdpr_audit"] = {
            "gdpr_compliant": False,
            "violations": [{"article": "Article 22", "issue": "Automated decisions"}],
            "data_flows": {"input": ["credit_history", "income"], "output": ["score"]},
        }
        return state

    @pytest.mark.asyncio
    async def test_generate_dpia_includes_sections(self, agent, sample_state):
        """Test DPIA generation includes required sections."""
        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                "# Data Protection Impact Assessment\n"
                "## 1. Description of Processing\n"
                "## 2. Necessity Assessment\n"
                "## 3. Risk Assessment\n"
                "## 4. Mitigation Measures\n",
                0.02,
            )

            content, cost = await agent._generate_dpia(sample_state, {})

            assert "Data Protection Impact Assessment" in content
            assert cost > 0

    @pytest.mark.asyncio
    async def test_generate_ropa_includes_sections(self, agent, sample_state):
        """Test ROPA generation includes required sections."""
        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                "# Record of Processing Activities\n"
                "## Processing Activity Details\n"
                "## Categories of Data\n",
                0.015,
            )

            content, cost = await agent._generate_ropa(sample_state, {})

            assert "Record of Processing Activities" in content
            assert cost > 0

    @pytest.mark.asyncio
    async def test_generate_conformity_assessment(self, agent, sample_state):
        """Test Conformity Assessment generation."""
        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                "# EU AI Act Conformity Assessment\n"
                "## System Identification\n"
                "## Requirements Assessment\n",
                0.025,
            )

            content, cost = await agent._generate_conformity_assessment(sample_state, {})

            assert "Conformity Assessment" in content
            assert cost > 0

    @pytest.mark.asyncio
    async def test_generate_transparency_notice(self, agent, sample_state):
        """Test Transparency Notice generation."""
        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = (
                "# AI System Transparency Notice\n"
                "## Notice to Users\n"
                "## Your Rights\n",
                0.01,
            )

            content, cost = await agent._generate_transparency_notice(sample_state, {})

            assert "Transparency Notice" in content
            assert cost > 0


class TestDocumentFilenames:
    """Tests for document filename generation."""

    @pytest.mark.asyncio
    async def test_document_filename_format(self):
        """Test that document filenames follow expected format."""
        from src.agents.documentation_generator import DocumentationGeneratorAgent

        agent = DocumentationGeneratorAgent()

        state = create_initial_state(
            system_description="Test AI system for compliance assessment with required documentation.",
            system_type="test_system",
            deployment_context="testing",
        )
        state["risk_classification"] = {"category": "HIGH_RISK"}
        state["gdpr_audit"] = {"dpia_required": True}

        with patch.object(agent, "invoke_llm", new_callable=AsyncMock) as mock_llm:
            mock_llm.return_value = ("# Document\n\nContent...", 0.01)

            result = await agent.execute(state)

            for doc in result["compliance_docs"]["documents"]:
                assert doc["filename"].endswith(".md")
                assert "_" in doc["filename"]  # timestamp separator
                # Check format is like "dpia_20240115_123456.md"
                parts = doc["filename"].split("_")
                assert len(parts) >= 2
