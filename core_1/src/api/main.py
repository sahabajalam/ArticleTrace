"""FastAPI application for AI Governance Monitoring.

Receives monitoring data from Projects 3 and 4,
performs compliance checks, and exposes metrics.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Query, Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.alerting.alert_manager import AlertManager, AlertSeverity
from src.compliance.eu_ai_act import Article14Monitor
from src.compliance.gdpr import GDPRMonitor
from src.config import get_settings
from src.database.models import (
    AlertLog,
    ComplianceViolation,
    DecisionLog,
    GraphRAGQueryLog,
)
from src.database.session import get_db, init_db
from src.monitoring.bias import BiasDetector
from src.monitoring.drift import DriftDetector
from src.monitoring.metrics import (
    init_metrics,
    record_agent_decision,
    record_graphrag_query,
    record_compliance_violation,
    update_open_violations,
    update_compliance_status,
)
from src.api.middleware import MetricsMiddleware
from src.api.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Initialize database
    try:
        init_db()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")

    # Initialize Prometheus metrics
    init_metrics()

    yield


app = FastAPI(
    title="AI Governance Monitoring API",
    description="Monitors Projects 3 & 4 for EU AI Act and GDPR compliance",
    version="1.0.0",
    lifespan=lifespan,
)

# Add rate limiter state
app.state.limiter = limiter

# Add exception handler for rate limits
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add metrics middleware
app.add_middleware(MetricsMiddleware)


# ============================================================================
# Request/Response Models
# ============================================================================


class AgentDecisionRequest(BaseModel):
    """Request to track agent decision from Project 4."""

    agent: str = Field(..., description="Agent name")
    input: dict[str, Any] = Field(..., description="Input data")
    prediction: str = Field(..., description="Prediction result")
    confidence: float = Field(..., ge=0.0, le=1.0)
    human_reviewed: bool = Field(default=False)
    human_override: bool = Field(default=False)
    timestamp: str | None = Field(default=None)
    metadata: dict[str, Any] = Field(default_factory=dict)
    processing_time_ms: float | None = Field(default=None)
    source: str = Field(default="project_4")


class GraphRAGQueryRequest(BaseModel):
    """Request to track GraphRAG query from Project 3."""

    query: str = Field(..., description="Query text")
    articles_retrieved: list[str] = Field(default_factory=list)
    reasoning_chains: list[Any] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    latency_ms: float = Field(..., description="Query latency")
    cost_usd: float = Field(default=0.0)
    timestamp: str | None = Field(default=None)
    error: str | None = Field(default=None)
    source: str = Field(default="project_3")


class ViolationResolutionRequest(BaseModel):
    """Request to resolve a compliance violation."""

    resolution_notes: str = Field(..., description="Resolution notes")
    resolved_by: str = Field(..., description="Who resolved it")


# ============================================================================
# Background Tasks
# ============================================================================


def run_compliance_checks(
    decision_id: str,
    db: Session,
) -> None:
    """Run all compliance checks for a decision."""
    decision = db.query(DecisionLog).filter(DecisionLog.id == decision_id).first()
    if not decision:
        return

    # EU AI Act Article 14 check
    article14_monitor = Article14Monitor(db)
    article14_result = article14_monitor.check_decision(decision)

    # GDPR Article 22 check
    gdpr_monitor = GDPRMonitor(db)
    gdpr_result = gdpr_monitor.check_decision(decision)

    # Send alerts for violations
    alert_manager = AlertManager(db)

    for violation in article14_result.violations:
        if violation["severity"] in ["HIGH", "CRITICAL"]:
            alert_manager.send_compliance_violation_alert(
                regulation="EU_AI_ACT",
                article="Article 14",
                severity=violation["severity"],
                description=violation["message"],
                recommendation=violation.get("recommendation"),
                related_decision_id=decision_id,
            )

    for violation in gdpr_result.violations:
        if violation["severity"] in ["HIGH", "CRITICAL"]:
            alert_manager.send_compliance_violation_alert(
                regulation="GDPR",
                article="Article 22",
                severity=violation["severity"],
                description=violation["message"],
                recommendation=violation.get("recommendation"),
                related_decision_id=decision_id,
            )


def run_bias_check(agent_name: str, db: Session) -> None:
    """Run bias detection for an agent."""
    bias_detector = BiasDetector(db)
    result = bias_detector.check_for_bias(agent_name, window_days=30)

    if result.get("bias_detected"):
        alert_manager = AlertManager(db)
        for bias_result in result.get("biased_attributes", []):
            alert_manager.send_bias_alert(
                agent_name=agent_name,
                attribute=bias_result["attribute"],
                p_value=bias_result["p_value"],
                details=bias_result,
            )


# ============================================================================
# API Endpoints
# ============================================================================


@app.get("/")
async def root() -> dict[str, Any]:
    """API information endpoint."""
    return {
        "name": "AI Governance Monitoring API",
        "version": "1.0.0",
        "description": "Monitors Projects 3 & 4 for compliance",
        "endpoints": {
            "track_decision": "/api/v1/monitoring/agent-decision",
            "track_graphrag": "/api/v1/monitoring/graphrag-query",
            "compliance_status": "/api/v1/compliance/status",
            "violations": "/api/v1/compliance/violations",
            "alerts": "/api/v1/alerts",
            "metrics": "/api/v1/metrics",
            "prometheus_metrics": "/metrics",
        },
    }


@app.get("/metrics")
async def prometheus_metrics() -> Response:
    """Expose Prometheus metrics endpoint."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/health")
async def health_check(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Health check endpoint."""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": db_status,
            "api": "healthy",
        },
    }


# ============================================================================
# Monitoring Endpoints
# ============================================================================


@app.post("/api/v1/monitoring/agent-decision")
@limiter.limit("60/minute")
async def track_agent_decision(
    http_request: Request,
    request: AgentDecisionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Receive agent decision from Project 4.

    Triggers background compliance checks:
    - EU AI Act Article 14 (human oversight)
    - GDPR Article 22 (automated decisions)
    - Bias detection
    """
    # Parse timestamp
    timestamp = (
        datetime.fromisoformat(request.timestamp)
        if request.timestamp
        else datetime.utcnow()
    )

    # Store decision
    decision = DecisionLog(
        timestamp=timestamp,
        agent_name=request.agent,
        source_project=request.source,
        prediction=request.prediction,
        confidence=request.confidence,
        human_reviewed=request.human_reviewed,
        human_override=request.human_override,
        input_data=request.input,
        output_data={"prediction": request.prediction, "confidence": request.confidence},
        metadata=request.metadata,
        processing_time_ms=request.processing_time_ms,
    )

    db.add(decision)
    db.commit()
    db.refresh(decision)

    # Record metrics
    record_agent_decision(
        agent_name=request.agent,
        prediction=request.prediction,
        confidence=request.confidence,
        human_reviewed=request.human_reviewed,
        human_override=request.human_override,
    )

    # Run compliance checks in background
    background_tasks.add_task(run_compliance_checks, decision.id, db)

    # Periodically run bias check (every 100 decisions)
    decision_count = (
        db.query(DecisionLog)
        .filter(DecisionLog.agent_name == request.agent)
        .count()
    )
    if decision_count % 100 == 0:
        background_tasks.add_task(run_bias_check, request.agent, db)

    return {
        "status": "success",
        "decision_id": decision.id,
        "timestamp": timestamp.isoformat(),
    }


@app.post("/api/v1/monitoring/graphrag-query")
@limiter.limit("60/minute")
async def track_graphrag_query(
    http_request: Request,
    request: GraphRAGQueryRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Receive GraphRAG query from Project 3."""
    timestamp = (
        datetime.fromisoformat(request.timestamp)
        if request.timestamp
        else datetime.utcnow()
    )

    query_log = GraphRAGQueryLog(
        timestamp=timestamp,
        query_text=request.query,
        articles_retrieved=request.articles_retrieved,
        reasoning_chains=request.reasoning_chains,
        confidence=request.confidence,
        citation_count=len(request.articles_retrieved),
        latency_ms=request.latency_ms,
        cost_usd=request.cost_usd,
        api_status_code=200 if not request.error else 500,
        error_message=request.error,
    )

    db.add(query_log)
    db.commit()

    # Record metrics
    record_graphrag_query(
        latency_ms=request.latency_ms,
        citation_count=len(request.articles_retrieved),
        cost_usd=request.cost_usd,
        success=request.error is None,
    )

    return {
        "status": "success",
        "query_id": query_log.id,
        "timestamp": timestamp.isoformat(),
    }


# ============================================================================
# Compliance Endpoints
# ============================================================================


@app.get("/api/v1/compliance/status")
@limiter.limit("120/minute")
async def get_compliance_status(request: Request, db: Session = Depends(get_db)) -> dict[str, Any]:
    """Get current compliance status for all regulations."""
    article14_monitor = Article14Monitor(db)
    gdpr_monitor = GDPRMonitor(db)

    article14_status = article14_monitor.get_compliance_status()
    gdpr_status = gdpr_monitor.get_compliance_status()

    # Update Prometheus metrics
    update_compliance_status("EU_AI_ACT", article14_status["status"] == "COMPLIANT")
    update_compliance_status("GDPR", gdpr_status["status"] == "COMPLIANT")
    update_open_violations("EU_AI_ACT", article14_status.get("open_violations", 0))
    update_open_violations("GDPR", gdpr_status.get("open_violations", 0))

    return {
        "eu_ai_act_article_14": article14_status["status"],
        "gdpr_article_22": gdpr_status["status"],
        "human_oversight_rate": article14_status.get("human_oversight_rate", 0),
        "active_violations": (
            article14_status.get("open_violations", 0)
            + gdpr_status.get("open_violations", 0)
        ),
        "details": {
            "eu_ai_act": article14_status,
            "gdpr": gdpr_status,
        },
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/compliance/violations")
@limiter.limit("60/minute")
async def get_violations(
    request: Request,
    status: str = Query(default="OPEN"),
    regulation: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get compliance violations."""
    query = db.query(ComplianceViolation)

    if status:
        query = query.filter(ComplianceViolation.status == status)
    if regulation:
        query = query.filter(ComplianceViolation.regulation == regulation)

    violations = query.order_by(ComplianceViolation.timestamp.desc()).limit(limit).all()

    return {
        "violations": [
            {
                "id": v.id,
                "timestamp": v.timestamp.isoformat(),
                "regulation": v.regulation,
                "article": v.article,
                "violation_type": v.violation_type,
                "severity": v.severity,
                "description": v.description,
                "status": v.status,
                "related_decision_id": v.related_decision_id,
            }
            for v in violations
        ],
        "total": len(violations),
    }


@app.post("/api/v1/compliance/violations/{violation_id}/resolve")
async def resolve_violation(
    violation_id: str,
    request: ViolationResolutionRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Resolve a compliance violation."""
    violation = (
        db.query(ComplianceViolation)
        .filter(ComplianceViolation.id == violation_id)
        .first()
    )

    if not violation:
        raise HTTPException(status_code=404, detail="Violation not found")

    violation.status = "RESOLVED"
    violation.resolved_at = datetime.utcnow()
    violation.resolution_notes = request.resolution_notes
    violation.resolved_by = request.resolved_by

    db.commit()

    return {
        "status": "success",
        "violation_id": violation_id,
        "resolved_at": violation.resolved_at.isoformat(),
    }


# ============================================================================
# Alerts Endpoints
# ============================================================================


@app.get("/api/v1/alerts")
async def get_alerts(
    limit: int = Query(default=50, le=200),
    acknowledged: bool | None = Query(default=None),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get recent alerts."""
    query = db.query(AlertLog)

    if acknowledged is not None:
        query = query.filter(AlertLog.acknowledged == acknowledged)

    alerts = query.order_by(AlertLog.timestamp.desc()).limit(limit).all()

    return {
        "alerts": [
            {
                "id": a.id,
                "timestamp": a.timestamp.isoformat(),
                "type": a.alert_type,
                "severity": a.severity,
                "title": a.title,
                "message": a.message,
                "acknowledged": a.acknowledged,
                "channels": a.channels,
            }
            for a in alerts
        ],
        "total": len(alerts),
    }


@app.post("/api/v1/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    acknowledged_by: str = Query(...),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Acknowledge an alert."""
    alert_manager = AlertManager(db)
    alert = alert_manager.acknowledge_alert(alert_id, acknowledged_by)

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    return {
        "status": "success",
        "alert_id": alert_id,
        "acknowledged_at": alert.acknowledged_at.isoformat(),
    }


# ============================================================================
# Metrics Endpoints
# ============================================================================


@app.get("/api/v1/metrics/agent/{agent_name}")
async def get_agent_metrics(
    agent_name: str,
    days: int = Query(default=7, le=90),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get metrics for a specific agent."""
    from datetime import timedelta

    since = datetime.utcnow() - timedelta(days=days)

    decisions = (
        db.query(DecisionLog)
        .filter(
            DecisionLog.agent_name == agent_name,
            DecisionLog.timestamp >= since,
        )
        .all()
    )

    if not decisions:
        return {
            "agent_name": agent_name,
            "message": "No decisions found",
            "days": days,
        }

    total = len(decisions)
    reviewed = sum(1 for d in decisions if d.human_reviewed)
    overridden = sum(1 for d in decisions if d.human_override)
    avg_confidence = sum(d.confidence for d in decisions) / total

    # Prediction distribution
    pred_dist: dict[str, int] = {}
    for d in decisions:
        pred_dist[d.prediction] = pred_dist.get(d.prediction, 0) + 1

    return {
        "agent_name": agent_name,
        "period_days": days,
        "total_decisions": total,
        "human_reviewed": reviewed,
        "human_review_rate": reviewed / total if total > 0 else 0,
        "human_overridden": overridden,
        "human_override_rate": overridden / total if total > 0 else 0,
        "avg_confidence": avg_confidence,
        "prediction_distribution": pred_dist,
    }


@app.get("/api/v1/metrics/graphrag")
async def get_graphrag_metrics(
    days: int = Query(default=7, le=90),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Get GraphRAG performance metrics."""
    from datetime import timedelta

    since = datetime.utcnow() - timedelta(days=days)

    queries = (
        db.query(GraphRAGQueryLog)
        .filter(GraphRAGQueryLog.timestamp >= since)
        .all()
    )

    if not queries:
        return {"message": "No queries found", "days": days}

    total = len(queries)
    errors = sum(1 for q in queries if q.error_message)
    avg_latency = sum(q.latency_ms for q in queries) / total
    avg_citations = sum(q.citation_count for q in queries) / total
    total_cost = sum(q.cost_usd for q in queries)

    return {
        "period_days": days,
        "total_queries": total,
        "error_count": errors,
        "error_rate": errors / total if total > 0 else 0,
        "avg_latency_ms": avg_latency,
        "avg_citations": avg_citations,
        "total_cost_usd": total_cost,
    }


@app.get("/api/v1/metrics/drift/{agent_name}")
async def check_drift(
    agent_name: str,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Check for drift in agent decisions."""
    drift_detector = DriftDetector(db)

    data_drift = drift_detector.check_data_drift(agent_name)
    prediction_drift = drift_detector.check_prediction_drift(agent_name)
    confidence_drift = drift_detector.check_confidence_drift(agent_name)

    return {
        "agent_name": agent_name,
        "data_drift": data_drift,
        "prediction_drift": prediction_drift,
        "confidence_drift": confidence_drift,
        "any_drift_detected": (
            data_drift.get("drift_detected", False)
            or prediction_drift.get("drift_detected", False)
            or confidence_drift.get("drift_detected", False)
        ),
    }


@app.get("/api/v1/metrics/bias/{agent_name}")
async def check_bias(
    agent_name: str,
    days: int = Query(default=30, le=90),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    """Check for bias in agent decisions."""
    bias_detector = BiasDetector(db)
    result = bias_detector.check_for_bias(agent_name, window_days=days)

    return {
        "agent_name": agent_name,
        "period_days": days,
        **result,
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
