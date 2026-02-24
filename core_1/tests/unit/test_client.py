"""Tests for monitoring client library."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.client.monitoring_client import (
    AgentDecision,
    GraphRAGQuery,
    MonitoringClient,
    SyncMonitoringClient,
)


class TestAgentDecision:
    """Test AgentDecision model."""

    def test_create_agent_decision(self):
        """Test creating agent decision."""
        decision = AgentDecision(
            agent="risk_classifier",
            input={"system": "facial recognition"},
            prediction="HIGH_RISK",
            confidence=0.92,
            human_reviewed=False,
        )

        assert decision.agent == "risk_classifier"
        assert decision.prediction == "HIGH_RISK"
        assert decision.confidence == 0.92
        assert not decision.human_reviewed

    def test_decision_with_metadata(self):
        """Test decision with metadata."""
        decision = AgentDecision(
            agent="risk_classifier",
            input={"system": "chatbot"},
            prediction="LIMITED_RISK",
            confidence=0.85,
            metadata={"user_informed": True},
        )

        assert decision.metadata["user_informed"] is True


class TestGraphRAGQuery:
    """Test GraphRAGQuery model."""

    def test_create_graphrag_query(self):
        """Test creating GraphRAG query."""
        query = GraphRAGQuery(
            query="Does GDPR require DPIA for facial recognition?",
            articles_retrieved=["GDPR Article 35", "GDPR Article 9"],
            confidence=0.87,
            latency_ms=1250.5,
            cost_usd=0.05,
        )

        assert query.query.startswith("Does GDPR")
        assert len(query.articles_retrieved) == 2
        assert query.latency_ms == 1250.5


class TestMonitoringClient:
    """Test async monitoring client."""

    @pytest.fixture
    def client(self):
        """Create monitoring client."""
        return MonitoringClient(api_url="http://localhost:8002")

    @pytest.mark.asyncio
    async def test_track_agent_decision_success(self, client):
        """Test tracking agent decision successfully."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_http_client = AsyncMock()
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_http_client.post.return_value = mock_response
            mock_get_client.return_value = mock_http_client

            decision = AgentDecision(
                agent="risk_classifier",
                input={"system": "test"},
                prediction="HIGH_RISK",
                confidence=0.9,
            )

            result = await client.track_agent_decision(decision)

            assert result is True
            mock_http_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_track_agent_decision_failure(self, client):
        """Test handling failed tracking."""
        with patch.object(client, "_get_client") as mock_get_client:
            mock_http_client = AsyncMock()
            mock_http_client.post.side_effect = Exception("Connection error")
            mock_get_client.return_value = mock_http_client

            decision = AgentDecision(
                agent="risk_classifier",
                input={"system": "test"},
                prediction="HIGH_RISK",
                confidence=0.9,
            )

            result = await client.track_agent_decision(decision)

            # Should return False but not raise
            assert result is False


class TestSyncMonitoringClient:
    """Test synchronous monitoring client."""

    def test_track_agent_decision(self):
        """Test sync tracking."""
        with patch("httpx.post") as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            client = SyncMonitoringClient(api_url="http://localhost:8002")

            decision = AgentDecision(
                agent="risk_classifier",
                input={"system": "test"},
                prediction="HIGH_RISK",
                confidence=0.9,
            )

            result = client.track_agent_decision(decision)

            assert result is True
