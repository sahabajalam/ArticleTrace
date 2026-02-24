"""Shared monitoring client used by Projects 3 & 4.

This client library should be installed in Projects 3 and 4 to send
monitoring data to the governance pipeline.

Usage in Project 4:
    from monitoring_client import MonitoringClient, AgentDecision

    monitor = MonitoringClient(api_url="http://localhost:8002")

    await monitor.track_agent_decision(AgentDecision(
        agent="risk_classifier",
        prediction="HIGH_RISK",
        confidence=0.92,
        input={"system": "facial recognition"},
        human_reviewed=False
    ))
"""

from datetime import datetime
from typing import Any

import httpx
from pydantic import BaseModel, Field


class AgentDecision(BaseModel):
    """Agent decision data model for Project 4."""

    agent: str = Field(..., description="Agent name (e.g., risk_classifier)")
    input: dict[str, Any] = Field(..., description="Input data for decision")
    prediction: str = Field(..., description="Prediction/classification result")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    human_reviewed: bool = Field(default=False, description="Was decision human-reviewed")
    human_override: bool = Field(default=False, description="Was decision overridden by human")
    timestamp: str | None = Field(default=None, description="ISO timestamp")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    processing_time_ms: float | None = Field(default=None, description="Processing time")


class GraphRAGQuery(BaseModel):
    """GraphRAG query data model for Project 3."""

    query: str = Field(..., description="Query text")
    articles_retrieved: list[str] = Field(default_factory=list, description="Retrieved articles")
    reasoning_chains: list[Any] = Field(default_factory=list, description="Reasoning chains")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Confidence score")
    latency_ms: float = Field(..., description="Query latency in milliseconds")
    cost_usd: float = Field(default=0.0, description="Cost in USD")
    timestamp: str | None = Field(default=None, description="ISO timestamp")
    error: str | None = Field(default=None, description="Error message if failed")


class ComplianceStatus(BaseModel):
    """Current compliance status."""

    eu_ai_act_article_14: str = Field(..., description="COMPLIANT or VIOLATION")
    gdpr_article_22: str = Field(..., description="COMPLIANT or VIOLATION")
    human_oversight_rate: float = Field(..., description="Human oversight rate")
    active_violations: int = Field(..., description="Number of active violations")
    active_alerts: list[dict[str, Any]] = Field(default_factory=list)
    last_updated: str = Field(..., description="ISO timestamp")


class MonitoringClient:
    """Client for sending monitoring data to Project 2.

    Usage:
        monitor = MonitoringClient(api_url="http://localhost:8002")

        # Track agent decision
        await monitor.track_agent_decision(AgentDecision(...))

        # Track GraphRAG query
        await monitor.track_graphrag_query(GraphRAGQuery(...))

        # Get compliance status
        status = await monitor.get_compliance_status()
    """

    def __init__(self, api_url: str, timeout: float = 10.0):
        """Initialize monitoring client.

        Args:
            api_url: Base URL of the monitoring API
            timeout: Request timeout in seconds
        """
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def track_agent_decision(self, decision: AgentDecision) -> bool:
        """Track Project 4 agent decision.

        Args:
            decision: Agent decision data

        Returns:
            True if successful, False otherwise
        """
        try:
            client = await self._get_client()
            data = decision.model_dump()
            data["timestamp"] = data.get("timestamp") or datetime.utcnow().isoformat()
            data["source"] = "project_4"

            response = await client.post(
                f"{self.api_url}/api/v1/monitoring/agent-decision",
                json=data,
            )
            return response.status_code == 200
        except Exception as e:
            # Log but don't crash monitored system
            print(f"Monitoring error (agent decision): {e}")
            return False

    async def track_graphrag_query(self, query: GraphRAGQuery) -> bool:
        """Track Project 3 GraphRAG query.

        Args:
            query: GraphRAG query data

        Returns:
            True if successful, False otherwise
        """
        try:
            client = await self._get_client()
            data = query.model_dump()
            data["timestamp"] = data.get("timestamp") or datetime.utcnow().isoformat()
            data["source"] = "project_3"

            response = await client.post(
                f"{self.api_url}/api/v1/monitoring/graphrag-query",
                json=data,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Monitoring error (graphrag query): {e}")
            return False

    async def get_compliance_status(self) -> ComplianceStatus | dict[str, Any]:
        """Get current compliance status.

        Returns:
            ComplianceStatus or error dict
        """
        try:
            client = await self._get_client()
            response = await client.get(f"{self.api_url}/api/v1/compliance/status")

            if response.status_code == 200:
                return ComplianceStatus(**response.json())
            return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    async def get_agent_metrics(self, agent_name: str) -> dict[str, Any]:
        """Get metrics for specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent metrics dict
        """
        try:
            client = await self._get_client()
            response = await client.get(
                f"{self.api_url}/api/v1/metrics/agent/{agent_name}"
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "MonitoringClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        await self.close()


# Synchronous wrapper for non-async code
class SyncMonitoringClient:
    """Synchronous wrapper for monitoring client."""

    def __init__(self, api_url: str, timeout: float = 10.0):
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout

    def track_agent_decision(self, decision: AgentDecision) -> bool:
        """Track agent decision synchronously."""
        try:
            data = decision.model_dump()
            data["timestamp"] = data.get("timestamp") or datetime.utcnow().isoformat()
            data["source"] = "project_4"

            response = httpx.post(
                f"{self.api_url}/api/v1/monitoring/agent-decision",
                json=data,
                timeout=self.timeout,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Monitoring error: {e}")
            return False

    def track_graphrag_query(self, query: GraphRAGQuery) -> bool:
        """Track GraphRAG query synchronously."""
        try:
            data = query.model_dump()
            data["timestamp"] = data.get("timestamp") or datetime.utcnow().isoformat()
            data["source"] = "project_3"

            response = httpx.post(
                f"{self.api_url}/api/v1/monitoring/graphrag-query",
                json=data,
                timeout=self.timeout,
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Monitoring error: {e}")
            return False

    def get_compliance_status(self) -> dict[str, Any]:
        """Get compliance status synchronously."""
        try:
            response = httpx.get(
                f"{self.api_url}/api/v1/compliance/status",
                timeout=self.timeout,
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
