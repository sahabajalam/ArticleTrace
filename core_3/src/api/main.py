"""FastAPI application for EU AI Act Compliance Automation Agent."""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.utils.logging import setup_logging, get_logger
from src.state.compliance_state import create_initial_state, ComplianceState
from src.agents.supervisor import SupervisorAgent
from src.control_plane.governance import control_plane
from src.control_plane.approval_queue import approval_queue
from src.database.session import init_db, get_db
from src.database.repository import AssessmentRepository
from src.cache.redis_client import get_redis_client, close_redis_client


# Setup logging
setup_logging(log_level=settings.log_level)
logger = get_logger(__name__)

# Global supervisor instance
supervisor: SupervisorAgent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    global supervisor
    logger.info("Starting EU AI Act Compliance Agent API")

    # Initialize database
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Could not initialize database: {e}")

    # Initialize Redis
    try:
        redis_client = await get_redis_client()
        if redis_client.is_connected:
            logger.info("Redis connected successfully")
        else:
            logger.warning("Redis not available, caching disabled")
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {e}")

    supervisor = SupervisorAgent()
    yield
    logger.info("Shutting down EU AI Act Compliance Agent API")
    if supervisor:
        await supervisor.close()

    # Close Redis connection
    await close_redis_client()


app = FastAPI(
    title="EU AI Act Compliance Automation Agent",
    description="Autonomous multi-agent system for EU AI Act compliance assessments",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware with environment-based configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AssessmentRequest(BaseModel):
    """Request to start a compliance assessment."""

    system_description: str = Field(
        ...,
        description="Detailed description of the AI system",
        min_length=50,
    )
    system_type: str = Field(
        ...,
        description="Type of AI system (e.g., facial_recognition, chatbot, credit_scoring)",
    )
    deployment_context: str = Field(
        ...,
        description="Context where the system will be deployed (e.g., employee_monitoring)",
    )
    company_name: str | None = Field(
        default=None,
        description="Name of the company/organization",
    )


class AssessmentResponse(BaseModel):
    """Response from starting an assessment."""

    session_id: str
    status: str
    message: str
    started_at: str


class AssessmentResult(BaseModel):
    """Full assessment result."""

    session_id: str
    status: str
    # Input fields
    system_description: str | None
    system_type: str | None
    company_name: str | None
    deployment_context: str | None
    # Agent outputs
    risk_classification: dict | None
    gdpr_audit: dict | None
    legal_citations: dict | None
    compliance_docs: dict | None
    final_report: dict | None
    errors: list[str]
    cost_tracking: dict
    completed_at: str | None


class ApprovalDecision(BaseModel):
    """Decision on an approval request."""

    decision: str = Field(..., pattern="^(approved|rejected)$")
    reviewer_id: str
    notes: str | None = None


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "name": "EU AI Act Compliance Automation Agent",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/v1/assessments": "Start a new compliance assessment",
            "GET /api/v1/assessments/{session_id}": "Get assessment status/results",
            "GET /api/v1/approvals": "List pending approvals",
            "POST /api/v1/approvals/{request_id}/decide": "Approve/reject a request",
            "GET /api/v1/statistics": "Get system statistics",
        },
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint."""
    db_status = "healthy"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "supervisor": "ready" if supervisor else "not_initialized",
            "control_plane": "ready",
            "approval_queue": "ready",
            "database": db_status,
        },
    }


@app.post("/api/v1/assessments", response_model=AssessmentResponse)
async def create_assessment(
    request: AssessmentRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Start a new compliance assessment.

    The assessment runs asynchronously. Use the session_id to check status.
    """
    if not supervisor:
        raise HTTPException(status_code=503, detail="Supervisor not initialized")

    # Create initial state
    state = create_initial_state(
        system_description=request.system_description,
        system_type=request.system_type,
        deployment_context=request.deployment_context,
        company_name=request.company_name,
    )

    session_id = state["session_id"]

    # Persist to database
    repo = AssessmentRepository(db)
    await repo.create(state)

    logger.info(
        "Assessment created",
        session_id=session_id,
        system_type=request.system_type,
    )

    # Run assessment in background
    background_tasks.add_task(run_assessment, session_id, state)

    return AssessmentResponse(
        session_id=session_id,
        status="started",
        message="Compliance assessment started. Use GET /api/v1/assessments/{session_id} to check status.",
        started_at=state["started_at"],
    )


async def run_assessment(session_id: str, state: ComplianceState):
    """Run the compliance assessment in background."""
    from src.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        repo = AssessmentRepository(db)

        try:
            logger.info("Running assessment", session_id=session_id)

            # Execute the workflow
            final_state = await supervisor.execute(state)

            # Update stored state in database
            await repo.update(session_id, final_state)

            logger.info(
                "Assessment completed",
                session_id=session_id,
                status=final_state.get("workflow_status"),
            )

        except Exception as e:
            logger.error(
                "Assessment failed",
                session_id=session_id,
                error=str(e),
            )
            state["workflow_status"] = "failed"
            state["errors"].append(str(e))
            await repo.update(session_id, state)


@app.get("/api/v1/assessments/{session_id}", response_model=AssessmentResult)
async def get_assessment(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get the status and results of an assessment."""
    repo = AssessmentRepository(db)
    state = await repo.get_state(session_id)

    if not state:
        raise HTTPException(status_code=404, detail="Assessment not found")

    return AssessmentResult(
        session_id=session_id,
        status=state.get("workflow_status", "unknown"),
        system_description=state.get("system_description"),
        system_type=state.get("system_type"),
        company_name=state.get("company_name"),
        deployment_context=state.get("deployment_context"),
        risk_classification=state.get("risk_classification"),
        gdpr_audit=state.get("gdpr_audit"),
        legal_citations=state.get("legal_citations"),
        compliance_docs=state.get("compliance_docs"),
        final_report=state.get("final_report"),
        errors=state.get("errors", []),
        cost_tracking=state.get("cost_tracking", {}),
        completed_at=state.get("completed_at"),
    )


@app.get("/api/v1/assessments")
async def list_assessments(
    status: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List all assessments."""
    repo = AssessmentRepository(db)
    results = await repo.list_all(status=status, limit=limit)

    return {"assessments": results, "total": len(results)}


@app.get("/api/v1/approvals")
async def list_approvals(agent: str | None = None):
    """List pending approval requests."""
    pending = approval_queue.get_pending_requests(agent_name=agent)

    return {
        "pending_approvals": [
            {
                "id": r.id,
                "agent": r.agent,
                "risk_level": r.risk_level,
                "created_at": r.created_at.isoformat(),
                "action": r.action,
            }
            for r in pending
        ],
        "total": len(pending),
    }


@app.get("/api/v1/approvals/{request_id}")
async def get_approval(request_id: str):
    """Get details of an approval request."""
    request = approval_queue.get_request(request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Approval request not found")

    return {
        "id": request.id,
        "agent": request.agent,
        "action": request.action,
        "context": request.context,
        "risk_level": request.risk_level,
        "status": request.status.value,
        "created_at": request.created_at.isoformat(),
        "reviewed_at": request.reviewed_at.isoformat() if request.reviewed_at else None,
        "reviewer_notes": request.reviewer_notes,
    }


@app.post("/api/v1/approvals/{request_id}/decide")
async def decide_approval(
    request_id: str,
    decision: ApprovalDecision,
    background_tasks: BackgroundTasks,
):
    """Approve or reject an approval request.

    If the request_id matches a session_id with a paused LangGraph workflow,
    this will resume the workflow after recording the human decision.
    """
    request = approval_queue.get_request(request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Approval request not found")

    if decision.decision == "approved":
        result = await approval_queue.approve(
            request_id,
            reviewer_id=decision.reviewer_id,
            notes=decision.notes,
        )
    else:
        result = await approval_queue.reject(
            request_id,
            reviewer_id=decision.reviewer_id,
            notes=decision.notes,
        )

    if not result:
        raise HTTPException(status_code=500, detail="Failed to process decision")

    # Resume the paused LangGraph workflow in background
    if supervisor and hasattr(result, "session_id"):
        background_tasks.add_task(
            resume_workflow, result.session_id, decision.decision
        )

    return {
        "id": result.id,
        "status": result.status.value,
        "reviewed_at": result.reviewed_at.isoformat(),
        "reviewer_id": result.reviewer_id,
    }


async def resume_workflow(session_id: str, decision: str):
    """Resume a paused workflow after human approval/rejection."""
    from src.database.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        repo = AssessmentRepository(db)

        try:
            logger.info("Resuming workflow", session_id=session_id, decision=decision)
            final_state = await supervisor.resume(session_id, decision)
            await repo.update(session_id, final_state)

            logger.info(
                "Workflow resumed and completed",
                session_id=session_id,
                status=final_state.get("workflow_status"),
            )
        except Exception as e:
            logger.error(
                "Workflow resume failed",
                session_id=session_id,
                error=str(e),
            )


@app.get("/api/v1/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    """Get system statistics."""
    repo = AssessmentRepository(db)
    status_counts = await repo.count_by_status()

    return {
        "control_plane": control_plane.get_statistics(),
        "approval_queue": approval_queue.get_statistics(),
        "assessments": {
            "total": sum(status_counts.values()),
            "by_status": status_counts,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/audit-log")
async def get_audit_log(agent: str | None = None, limit: int = 100):
    """Get audit log entries."""
    logs = control_plane.get_audit_log(agent_name=agent, limit=limit)
    return {"audit_log": logs, "total": len(logs)}


@app.get("/api/v1/documents/{session_id}")
async def get_documents(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get generated compliance documents for an assessment."""
    repo = AssessmentRepository(db)
    state = await repo.get_state(session_id)

    if not state:
        raise HTTPException(status_code=404, detail="Assessment not found")

    docs = state.get("compliance_docs", {})

    if not docs:
        raise HTTPException(status_code=404, detail="No documents generated yet")

    return {
        "session_id": session_id,
        "documents": docs.get("documents", []),
        "required_docs": docs.get("required_docs", []),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
