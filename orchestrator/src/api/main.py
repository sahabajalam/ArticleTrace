"""FastAPI application for the ArticleTrace scan orchestrator."""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.supervisor import SupervisorAgent
from src.api.scans import router as scans_router
from src.cache.redis_client import close_redis_client, get_redis_client
from src.config import settings
from src.control_plane.governance import control_plane
from src.database.repository import ScanRepository
from src.database.session import get_db, init_db
from src.utils.logging import get_logger, setup_logging


setup_logging(log_level=settings.log_level)
logger = get_logger(__name__)

# Global supervisor instance (lazily set in lifespan; scans.py reads it).
supervisor: SupervisorAgent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global supervisor
    logger.info("Starting orchestrator API")

    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.warning(f"Database init skipped: {e}")

    try:
        redis_client = await get_redis_client()
        if redis_client.is_connected:
            logger.info("Redis connected")
        else:
            logger.warning("Redis unavailable, caching disabled")
    except Exception as e:
        logger.warning(f"Redis init skipped: {e}")

    supervisor = SupervisorAgent()
    yield

    logger.info("Shutting down orchestrator API")
    if supervisor:
        await supervisor.close()
    await close_redis_client()


app = FastAPI(
    title="ArticleTrace Scan Orchestrator",
    description="Repository-based EU AI Act / GDPR compliance scanner",
    version="2.0.0",
    lifespan=lifespan,
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans_router)


@app.get("/")
async def root():
    return {
        "name": "ArticleTrace Scan Orchestrator",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/v1/scans": "Start a new repository scan",
            "GET /api/v1/scans": "List scans",
            "GET /api/v1/scans/{id}": "Full scan record",
            "GET /api/v1/scans/{id}/findings": "Flat findings list",
            "GET /api/v1/scans/{id}/report": "Synthesized ScanReport",
            "GET /api/v1/statistics": "System statistics",
            "GET /api/v1/audit-log": "Control-plane audit log",
        },
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "unavailable"
    if db is not None:
        try:
            await db.execute(text("SELECT 1"))
            db_status = "healthy"
        except Exception:
            db_status = "unhealthy"
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "supervisor": "ready" if supervisor else "not_initialized",
            "control_plane": "ready",
            "database": db_status,
        },
    }


@app.get("/api/v1/statistics")
async def get_statistics(db: AsyncSession = Depends(get_db)):
    repo = ScanRepository(db)
    status_counts = await repo.count_by_status()
    return {
        "control_plane": control_plane.get_statistics(),
        "scans": {
            "total": sum(status_counts.values()),
            "by_status": status_counts,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/audit-log")
async def get_audit_log(agent: str | None = None, limit: int = 100):
    logs = control_plane.get_audit_log(agent_name=agent, limit=limit)
    return {"audit_log": logs, "total": len(logs)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
    )
