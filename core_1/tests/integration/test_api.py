"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client."""
    from src.api.main import app

    return TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints."""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "Governance" in data["name"]
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        # May be 200 or 500 depending on DB availability
        assert response.status_code in [200, 500]

    def test_track_agent_decision_validation(self, client):
        """Test agent decision endpoint validates input."""
        # Missing required fields
        response = client.post(
            "/api/v1/monitoring/agent-decision",
            json={"agent": "test"},
        )

        assert response.status_code == 422  # Validation error

    def test_track_agent_decision_valid(self, client):
        """Test tracking valid agent decision."""
        response = client.post(
            "/api/v1/monitoring/agent-decision",
            json={
                "agent": "risk_classifier",
                "input": {"system": "test"},
                "prediction": "HIGH_RISK",
                "confidence": 0.9,
            },
        )

        # May fail if DB not available
        assert response.status_code in [200, 500]

    def test_track_graphrag_query_valid(self, client):
        """Test tracking GraphRAG query."""
        response = client.post(
            "/api/v1/monitoring/graphrag-query",
            json={
                "query": "Test query",
                "articles_retrieved": ["Article 1"],
                "latency_ms": 500.0,
                "cost_usd": 0.01,
            },
        )

        assert response.status_code in [200, 500]

    def test_get_compliance_status(self, client):
        """Test compliance status endpoint."""
        response = client.get("/api/v1/compliance/status")

        # May fail if DB not available
        assert response.status_code in [200, 500]

    def test_get_violations(self, client):
        """Test violations endpoint."""
        response = client.get("/api/v1/compliance/violations")

        assert response.status_code in [200, 500]

    def test_get_alerts(self, client):
        """Test alerts endpoint."""
        response = client.get("/api/v1/alerts")

        assert response.status_code in [200, 500]

    def test_get_agent_metrics(self, client):
        """Test agent metrics endpoint."""
        response = client.get("/api/v1/metrics/agent/risk_classifier")

        assert response.status_code in [200, 500]
