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
        assert "EU AI Act" in data["name"]
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_create_assessment_validation(self, client):
        """Test assessment creation validates input."""
        # Too short description
        response = client.post(
            "/api/v1/assessments",
            json={
                "system_description": "Short",
                "system_type": "test",
                "deployment_context": "test",
            },
        )

        assert response.status_code == 422  # Validation error

    def test_get_nonexistent_assessment(self, client):
        """Test getting non-existent assessment returns 404."""
        response = client.get("/api/v1/assessments/nonexistent-id")

        assert response.status_code == 404

    def test_list_assessments_empty(self, client):
        """Test listing assessments when empty."""
        response = client.get("/api/v1/assessments")

        assert response.status_code == 200
        data = response.json()
        assert "assessments" in data

    def test_list_approvals(self, client):
        """Test listing approvals."""
        response = client.get("/api/v1/approvals")

        assert response.status_code == 200
        data = response.json()
        assert "pending_approvals" in data
        assert "total" in data

    def test_get_statistics(self, client):
        """Test getting statistics."""
        response = client.get("/api/v1/statistics")

        assert response.status_code == 200
        data = response.json()
        assert "control_plane" in data
        assert "approval_queue" in data

    def test_get_audit_log(self, client):
        """Test getting audit log."""
        response = client.get("/api/v1/audit-log")

        assert response.status_code == 200
        data = response.json()
        assert "audit_log" in data
