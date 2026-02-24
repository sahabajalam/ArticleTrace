"""Prometheus metrics definitions for AI Governance Monitoring."""

from prometheus_client import Counter, Histogram, Gauge, Info

# API Request metrics
REQUEST_COUNT = Counter(
    "monitoring_api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "monitoring_api_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Agent Decision metrics
AGENT_DECISIONS_TOTAL = Counter(
    "agent_decisions_total",
    "Total number of agent decisions tracked",
    ["agent_name", "prediction"],
)

AGENT_DECISION_CONFIDENCE = Histogram(
    "agent_decision_confidence",
    "Distribution of agent decision confidence scores",
    ["agent_name"],
    buckets=[0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99, 1.0],
)

HUMAN_REVIEWED_DECISIONS = Counter(
    "human_reviewed_decisions_total",
    "Total number of human-reviewed decisions",
    ["agent_name"],
)

HUMAN_OVERRIDDEN_DECISIONS = Counter(
    "human_overridden_decisions_total",
    "Total number of human-overridden decisions",
    ["agent_name"],
)

# Compliance metrics
COMPLIANCE_VIOLATIONS = Counter(
    "compliance_violations_total",
    "Total number of compliance violations detected",
    ["regulation", "article", "severity"],
)

OPEN_VIOLATIONS = Gauge(
    "compliance_violations_open",
    "Current number of open compliance violations",
    ["regulation"],
)

COMPLIANCE_STATUS = Gauge(
    "compliance_status",
    "Overall compliance status (1=compliant, 0=non-compliant)",
    ["regulation"],
)

# GraphRAG metrics
GRAPHRAG_QUERIES_TOTAL = Counter(
    "graphrag_queries_total",
    "Total number of GraphRAG queries",
    ["status"],
)

GRAPHRAG_LATENCY = Histogram(
    "graphrag_query_latency_ms",
    "GraphRAG query latency in milliseconds",
    buckets=[50, 100, 250, 500, 1000, 2500, 5000, 10000],
)

GRAPHRAG_CITATIONS = Histogram(
    "graphrag_citations_count",
    "Number of citations returned per query",
    buckets=[0, 1, 2, 5, 10, 20, 50],
)

GRAPHRAG_COST = Counter(
    "graphrag_cost_usd_total",
    "Total cost of GraphRAG queries in USD",
)

# Drift and Bias metrics
DRIFT_DETECTED = Counter(
    "drift_detected_total",
    "Total number of drift detections",
    ["agent_name", "drift_type"],
)

BIAS_DETECTED = Counter(
    "bias_detected_total",
    "Total number of bias detections",
    ["agent_name", "attribute"],
)

# Alerting metrics
ALERTS_SENT = Counter(
    "alerts_sent_total",
    "Total number of alerts sent",
    ["severity", "channel"],
)

ALERTS_ACKNOWLEDGED = Counter(
    "alerts_acknowledged_total",
    "Total number of alerts acknowledged",
)

# System info
APP_INFO = Info(
    "monitoring_app",
    "Application information",
)


def init_metrics():
    """Initialize static metric values."""
    APP_INFO.info({
        "version": "1.0.0",
        "name": "ai-governance-monitoring",
    })


def record_api_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record an API request."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status_code=str(status_code)).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)


def record_agent_decision(
    agent_name: str,
    prediction: str,
    confidence: float,
    human_reviewed: bool = False,
    human_override: bool = False,
):
    """Record an agent decision."""
    AGENT_DECISIONS_TOTAL.labels(agent_name=agent_name, prediction=prediction).inc()
    AGENT_DECISION_CONFIDENCE.labels(agent_name=agent_name).observe(confidence)

    if human_reviewed:
        HUMAN_REVIEWED_DECISIONS.labels(agent_name=agent_name).inc()
    if human_override:
        HUMAN_OVERRIDDEN_DECISIONS.labels(agent_name=agent_name).inc()


def record_compliance_violation(regulation: str, article: str, severity: str):
    """Record a compliance violation."""
    COMPLIANCE_VIOLATIONS.labels(
        regulation=regulation,
        article=article,
        severity=severity,
    ).inc()


def update_open_violations(regulation: str, count: int):
    """Update the count of open violations for a regulation."""
    OPEN_VIOLATIONS.labels(regulation=regulation).set(count)


def update_compliance_status(regulation: str, is_compliant: bool):
    """Update compliance status for a regulation."""
    COMPLIANCE_STATUS.labels(regulation=regulation).set(1 if is_compliant else 0)


def record_graphrag_query(
    latency_ms: float,
    citation_count: int,
    cost_usd: float,
    success: bool = True,
):
    """Record a GraphRAG query."""
    status = "success" if success else "error"
    GRAPHRAG_QUERIES_TOTAL.labels(status=status).inc()
    GRAPHRAG_LATENCY.observe(latency_ms)
    GRAPHRAG_CITATIONS.observe(citation_count)
    GRAPHRAG_COST.inc(cost_usd)


def record_drift(agent_name: str, drift_type: str):
    """Record a drift detection event."""
    DRIFT_DETECTED.labels(agent_name=agent_name, drift_type=drift_type).inc()


def record_bias(agent_name: str, attribute: str):
    """Record a bias detection event."""
    BIAS_DETECTED.labels(agent_name=agent_name, attribute=attribute).inc()


def record_alert(severity: str, channel: str):
    """Record an alert sent."""
    ALERTS_SENT.labels(severity=severity, channel=channel).inc()


def record_alert_acknowledged():
    """Record an alert acknowledgment."""
    ALERTS_ACKNOWLEDGED.inc()
