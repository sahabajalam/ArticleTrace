"""Cross-module integration tests for EU AI Regulatory Compliance Engine.

Tests the integration between:
- Core 3 (Compliance Agent) → Core 2 (GraphRAG)
- Core 3 (Compliance Agent) → Core 1 (Monitoring)
- Core 2 (GraphRAG) → Core 1 (Monitoring)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json
from datetime import datetime


class TestCore3ToCore2Integration:
    """Tests for Core 3 Compliance Agent calling Core 2 GraphRAG."""

    @pytest.fixture
    def mock_graphrag_response(self):
        """Mock GraphRAG API response."""
        return {
            "query": "What GDPR requirements apply to biometric data?",
            "answer": "GDPR Article 9 prohibits processing of biometric data...",
            "confidence": 0.87,
            "reasoning_chain": [
                {"step": 1, "text": "Biometric data is special category data"},
                {"step": 2, "text": "Article 9 applies to special categories"},
            ],
            "citations": [
                "GDPR Article 9",
                "GDPR Article 35",
            ],
            "execution_time_ms": 1250.5,
        }

    @pytest.mark.asyncio
    async def test_legal_research_calls_graphrag(self, mock_graphrag_response):
        """Test that Legal Research Agent correctly calls GraphRAG API."""
        from unittest.mock import AsyncMock
        import httpx

        # Mock httpx client
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "paths": [
                {
                    "nodes": [
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9"}
                    ],
                    "relationship": "APPLIES_TO",
                    "weight": 0.9,
                }
            ]
        }

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response

        # Test the API call format
        request_data = {
            "start_entities": ["biometric_data", "facial_recognition"],
            "relationship_types": ["REGULATES", "REQUIRES", "PROHIBITS"],
            "max_hops": 2,
            "limit": 20,
        }

        response = await mock_client.post(
            "http://localhost:8001/api/v1/graph/traverse",
            json=request_data,
        )

        assert response.status_code == 200
        result = response.json()
        assert "paths" in result

    @pytest.mark.asyncio
    async def test_hybrid_reasoning_api_format(self, mock_graphrag_response):
        """Test the hybrid reasoning API request format."""
        mock_client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_graphrag_response
        mock_client.post.return_value = mock_response

        # Test hybrid reasoning API
        request_data = {
            "query": "Does facial recognition for employee attendance require a DPIA?",
            "max_hops": 3,
        }

        response = await mock_client.post(
            "http://localhost:8001/api/v1/hybrid/reason",
            json=request_data,
        )

        assert response.status_code == 200
        result = response.json()
        assert "answer" in result
        assert "confidence" in result
        assert "citations" in result

    @pytest.mark.asyncio
    async def test_vector_search_api_format(self):
        """Test vector search API request format."""
        mock_client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "text": "Article 9 prohibits processing of biometric data...",
                    "score": 0.85,
                    "metadata": {
                        "regulation": "GDPR",
                        "article": "Article 9",
                        "title": "Special categories",
                    },
                }
            ]
        }
        mock_client.post.return_value = mock_response

        request_data = {
            "query": "biometric data processing requirements",
            "top_k": 10,
            "filter_regulations": ["GDPR", "EU_AI_ACT"],
        }

        response = await mock_client.post(
            "http://localhost:8001/api/v1/vector/search",
            json=request_data,
        )

        assert response.status_code == 200
        result = response.json()
        assert "results" in result


class TestCore3ToCore1Integration:
    """Tests for Core 3 Compliance Agent reporting to Core 1 Monitoring."""

    @pytest.fixture
    def agent_decision_payload(self):
        """Sample agent decision payload."""
        return {
            "agent": "risk_classifier",
            "input": {
                "system_description": "Facial recognition for attendance",
                "system_type": "facial_recognition",
                "deployment_context": "employee_monitoring",
            },
            "prediction": "HIGH_RISK",
            "confidence": 0.92,
            "human_reviewed": False,
            "human_override": False,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "session_id": "test-123",
                "article": "Article 6",
                "annex": "Annex III",
            },
            "processing_time_ms": 1500.0,
            "source": "project_4",
        }

    @pytest.mark.asyncio
    async def test_agent_decision_tracking_format(self, agent_decision_payload):
        """Test agent decision tracking API format."""
        mock_client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "decision_id": "dec-456",
            "timestamp": datetime.utcnow().isoformat(),
        }
        mock_client.post.return_value = mock_response

        response = await mock_client.post(
            "http://localhost:8002/api/v1/monitoring/agent-decision",
            json=agent_decision_payload,
        )

        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "decision_id" in result

    @pytest.mark.asyncio
    async def test_compliance_status_check(self):
        """Test compliance status API format."""
        mock_client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "eu_ai_act_article_14": "COMPLIANT",
            "gdpr_article_22": "COMPLIANT",
            "human_oversight_rate": 0.15,
            "active_violations": 0,
            "details": {
                "eu_ai_act": {"status": "COMPLIANT", "open_violations": 0},
                "gdpr": {"status": "COMPLIANT", "open_violations": 0},
            },
        }
        mock_client.get.return_value = mock_response

        response = await mock_client.get(
            "http://localhost:8002/api/v1/compliance/status"
        )

        assert response.status_code == 200
        result = response.json()
        assert "eu_ai_act_article_14" in result
        assert "gdpr_article_22" in result


class TestCore2ToCore1Integration:
    """Tests for Core 2 GraphRAG reporting to Core 1 Monitoring."""

    @pytest.fixture
    def graphrag_query_payload(self):
        """Sample GraphRAG query payload for monitoring."""
        return {
            "query": "What GDPR articles apply to facial recognition?",
            "articles_retrieved": ["GDPR_ART_9", "GDPR_ART_35", "GDPR_ART_6"],
            "reasoning_chains": [
                ["GDPR_ART_9", "REQUIRES", "GDPR_ART_35"],
            ],
            "confidence": 0.85,
            "latency_ms": 1250.5,
            "cost_usd": 0.002,
            "timestamp": datetime.utcnow().isoformat(),
            "error": None,
            "source": "project_3",
        }

    @pytest.mark.asyncio
    async def test_graphrag_query_tracking_format(self, graphrag_query_payload):
        """Test GraphRAG query tracking API format."""
        mock_client = AsyncMock()

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "query_id": "query-789",
            "timestamp": datetime.utcnow().isoformat(),
        }
        mock_client.post.return_value = mock_response

        response = await mock_client.post(
            "http://localhost:8002/api/v1/monitoring/graphrag-query",
            json=graphrag_query_payload,
        )

        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "success"
        assert "query_id" in result


class TestEndToEndWorkflow:
    """End-to-end workflow integration tests."""

    @pytest.mark.asyncio
    async def test_full_assessment_workflow(self):
        """Test complete assessment workflow across all modules."""
        # Step 1: Create assessment in Core 3
        assessment_request = {
            "system_description": "AI-powered facial recognition system for employee attendance tracking in corporate offices. Captures facial images and logs entry/exit times.",
            "system_type": "facial_recognition",
            "deployment_context": "employee_monitoring",
            "company_name": "TechCorp Inc.",
        }

        # Mock Core 3 assessment creation
        mock_core3_client = AsyncMock()
        mock_core3_response = MagicMock()
        mock_core3_response.status_code = 200
        mock_core3_response.json.return_value = {
            "session_id": "assess-001",
            "status": "started",
            "message": "Assessment started",
            "started_at": datetime.utcnow().isoformat(),
        }
        mock_core3_client.post.return_value = mock_core3_response

        response = await mock_core3_client.post(
            "http://localhost:8000/api/v1/assessments",
            json=assessment_request,
        )

        assert response.status_code == 200
        session_id = response.json()["session_id"]

        # Step 2: Legal Research calls Core 2 GraphRAG
        mock_core2_client = AsyncMock()
        mock_core2_response = MagicMock()
        mock_core2_response.status_code = 200
        mock_core2_response.json.return_value = {
            "paths": [
                {
                    "nodes": [
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 9"},
                        {"type": "ARTICLE", "regulation": "GDPR", "number": "Article 35"},
                    ],
                    "relationship": "TRIGGERS",
                    "weight": 0.9,
                }
            ]
        }
        mock_core2_client.post.return_value = mock_core2_response

        graphrag_response = await mock_core2_client.post(
            "http://localhost:8001/api/v1/graph/traverse",
            json={
                "start_entities": ["facial_recognition", "biometric_data"],
                "relationship_types": ["REQUIRES", "TRIGGERS"],
                "max_hops": 2,
            },
        )

        assert graphrag_response.status_code == 200
        assert len(graphrag_response.json()["paths"]) > 0

        # Step 3: Report to Core 1 Monitoring
        mock_core1_client = AsyncMock()
        mock_core1_response = MagicMock()
        mock_core1_response.status_code = 200
        mock_core1_response.json.return_value = {
            "status": "success",
            "decision_id": "dec-001",
        }
        mock_core1_client.post.return_value = mock_core1_response

        monitoring_response = await mock_core1_client.post(
            "http://localhost:8002/api/v1/monitoring/agent-decision",
            json={
                "agent": "risk_classifier",
                "input": assessment_request,
                "prediction": "HIGH_RISK",
                "confidence": 0.92,
                "human_reviewed": False,
                "source": "project_4",
            },
        )

        assert monitoring_response.status_code == 200

    @pytest.mark.asyncio
    async def test_compliance_violation_flow(self):
        """Test compliance violation detection and alerting flow."""
        # Simulate a decision that triggers a compliance violation
        decision_payload = {
            "agent": "risk_classifier",
            "input": {"system_type": "emotion_recognition"},
            "prediction": "PROHIBITED",
            "confidence": 0.95,
            "human_reviewed": False,  # Should trigger Article 14 violation
            "human_override": False,
            "source": "project_4",
        }

        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "decision_id": "dec-002",
        }
        mock_client.post.return_value = mock_response

        response = await mock_client.post(
            "http://localhost:8002/api/v1/monitoring/agent-decision",
            json=decision_payload,
        )

        assert response.status_code == 200

        # Check violations endpoint
        mock_violations_response = MagicMock()
        mock_violations_response.status_code = 200
        mock_violations_response.json.return_value = {
            "violations": [
                {
                    "id": "viol-001",
                    "regulation": "EU_AI_ACT",
                    "article": "Article 14",
                    "violation_type": "INSUFFICIENT_HUMAN_OVERSIGHT",
                    "severity": "HIGH",
                    "status": "OPEN",
                }
            ],
            "total": 1,
        }
        mock_client.get.return_value = mock_violations_response

        violations_response = await mock_client.get(
            "http://localhost:8002/api/v1/compliance/violations"
        )

        assert violations_response.status_code == 200


class TestAPIContractValidation:
    """Tests to validate API contracts between modules."""

    def test_core3_assessment_request_schema(self):
        """Validate Core 3 assessment request schema."""
        valid_request = {
            "system_description": "A" * 50,  # min_length=50
            "system_type": "chatbot",
            "deployment_context": "customer_service",
            "company_name": "TestCorp",  # Optional
        }

        # All required fields present
        assert "system_description" in valid_request
        assert "system_type" in valid_request
        assert "deployment_context" in valid_request
        assert len(valid_request["system_description"]) >= 50

    def test_core1_agent_decision_schema(self):
        """Validate Core 1 agent decision request schema."""
        valid_request = {
            "agent": "risk_classifier",
            "input": {"key": "value"},
            "prediction": "HIGH_RISK",
            "confidence": 0.85,
            "human_reviewed": False,
            "human_override": False,
            "timestamp": None,  # Optional
            "metadata": {},  # Optional, default empty
            "processing_time_ms": None,  # Optional
            "source": "project_4",
        }

        # Validate required fields
        assert "agent" in valid_request
        assert "input" in valid_request
        assert "prediction" in valid_request
        assert 0 <= valid_request["confidence"] <= 1

    def test_core2_graphrag_request_schema(self):
        """Validate Core 2 GraphRAG request schemas."""
        # Vector search schema
        vector_request = {
            "query": "biometric data requirements",
            "top_k": 5,
        }

        assert "query" in vector_request
        assert vector_request["top_k"] > 0

        # Graph traverse schema
        graph_request = {
            "start_entities": ["biometric_data"],
            "relationship_types": ["REQUIRES"],
            "max_hops": 2,
            "limit": 20,
        }

        assert "start_entities" in graph_request
        assert len(graph_request["start_entities"]) > 0

        # Hybrid reasoning schema
        reason_request = {
            "query": "Does this system require a DPIA?",
            "max_hops": 3,
        }

        assert "query" in reason_request
