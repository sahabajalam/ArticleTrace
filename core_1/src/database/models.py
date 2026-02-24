"""Database models for governance monitoring.

Stores decision logs, compliance violations, and alerts for
Projects 3 and 4 monitoring.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def generate_uuid() -> str:
    """Generate UUID string."""
    return str(uuid.uuid4())


class DecisionLog(Base):
    """Stores every agent decision from Project 4.

    Used for:
    - EU AI Act Article 14 compliance (human oversight)
    - GDPR Article 22 compliance (automated decisions)
    - Drift detection
    - Bias detection
    """

    __tablename__ = "decision_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Agent info
    agent_name = Column(String(100), nullable=False, index=True)
    source_project = Column(String(50), default="project_4")

    # Decision details
    prediction = Column(String(100), nullable=False, index=True)
    confidence = Column(Float, nullable=False)
    human_reviewed = Column(Boolean, default=False, index=True)
    human_override = Column(Boolean, default=False)

    # Data
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)

    # Performance
    processing_time_ms = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_decision_agent_timestamp", "agent_name", "timestamp"),
        Index("ix_decision_prediction", "prediction"),
    )


class GraphRAGQueryLog(Base):
    """Stores every GraphRAG query from Project 3.

    Used for:
    - Performance monitoring
    - Cost tracking
    - Quality assessment
    """

    __tablename__ = "graphrag_query_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Query details
    query_text = Column(Text, nullable=False)
    articles_retrieved = Column(JSON, nullable=True)
    reasoning_chains = Column(JSON, nullable=True)

    # Quality
    confidence = Column(Float, nullable=True)
    citation_count = Column(Integer, default=0)

    # Performance
    latency_ms = Column(Float, nullable=False)
    cost_usd = Column(Float, default=0.0)

    # Health
    api_status_code = Column(Integer, default=200)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("ix_graphrag_timestamp", "timestamp"),)


class ComplianceViolation(Base):
    """Stores detected compliance violations.

    Types:
    - EU AI Act Article 14 (human oversight)
    - GDPR Article 22 (automated decisions)
    - Bias detection
    - Drift detection
    """

    __tablename__ = "compliance_violations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Violation details
    regulation = Column(String(50), nullable=False, index=True)  # EU_AI_ACT, GDPR
    article = Column(String(50), nullable=False)  # Article 14, Article 22
    violation_type = Column(String(200), nullable=False)
    severity = Column(String(20), nullable=False, index=True)  # LOW, MEDIUM, HIGH, CRITICAL

    # Context
    related_decision_id = Column(String(36), nullable=True, index=True)
    description = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=True)

    # Resolution
    status = Column(String(20), default="OPEN", index=True)  # OPEN, ACKNOWLEDGED, RESOLVED
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    resolved_by = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_violation_regulation_status", "regulation", "status"),
        Index("ix_violation_severity", "severity"),
    )


class AlertLog(Base):
    """Stores all alerts sent.

    Tracks notification history for compliance auditing.
    """

    __tablename__ = "alert_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)

    # Alert details
    alert_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)

    # Related entities
    related_violation_id = Column(String(36), nullable=True)
    related_decision_id = Column(String(36), nullable=True)

    # Notification
    channels = Column(JSON, nullable=True)  # ["slack", "email"]
    sent_successfully = Column(Boolean, default=True)
    send_error = Column(Text, nullable=True)

    # Acknowledgment
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
    acknowledged_by = Column(String(100), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class AgentMetrics(Base):
    """Aggregated metrics per agent per time window.

    Pre-computed for dashboard performance.
    """

    __tablename__ = "agent_metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    agent_name = Column(String(100), nullable=False, index=True)
    window_start = Column(DateTime, nullable=False, index=True)
    window_end = Column(DateTime, nullable=False)

    # Counts
    total_decisions = Column(Integer, default=0)
    human_reviewed_count = Column(Integer, default=0)
    human_override_count = Column(Integer, default=0)

    # Rates
    human_review_rate = Column(Float, default=0.0)
    human_override_rate = Column(Float, default=0.0)
    avg_confidence = Column(Float, default=0.0)

    # Distribution
    prediction_distribution = Column(JSON, nullable=True)

    # Compliance
    violations_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_agent_metrics_window", "agent_name", "window_start"),
    )


class DriftReport(Base):
    """Stores drift detection reports."""

    __tablename__ = "drift_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)
    agent_name = Column(String(100), nullable=False, index=True)

    # Drift metrics
    drift_detected = Column(Boolean, default=False)
    drift_score = Column(Float, nullable=True)
    drift_type = Column(String(50), nullable=True)  # data, prediction, concept

    # Details
    report_data = Column(JSON, nullable=True)
    drifted_features = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class BiasReport(Base):
    """Stores bias detection reports."""

    __tablename__ = "bias_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime, nullable=False, index=True)
    agent_name = Column(String(100), nullable=False, index=True)

    # Bias metrics
    bias_detected = Column(Boolean, default=False)
    protected_attribute = Column(String(100), nullable=True)
    p_value = Column(Float, nullable=True)
    chi_square_statistic = Column(Float, nullable=True)

    # Details
    contingency_table = Column(JSON, nullable=True)
    analysis_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
