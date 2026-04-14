"""Scan API — the primary entry point.

POST /api/v1/scans               start a repo scan
GET  /api/v1/scans               list scans
GET  /api/v1/scans/{id}          full scan record (profile + posture + narrative)
GET  /api/v1/scans/{id}/findings flat findings list
GET  /api/v1/scans/{id}/report   the synthesized ScanReport
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime
from typing import Any, Literal

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession

from src.code_analyzer import run_scan
from src.database.repository import ScanRepository
from src.database.session import get_db
from src.state.scan_state import create_initial_state

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/scans", tags=["scans"])


class ScanRequest(BaseModel):
    repo_url: HttpUrl = Field(..., description="Public Git repo URL")
    ref: str = Field("main", description="Branch or tag to scan")
    enrich_with_kg: bool = Field(
        True, description="Run the LangGraph supervisor (KG + narrative)"
    )


class ScanSummary(BaseModel):
    scan_id: str
    status: Literal["queued", "running", "completed", "failed"]
    repo_url: str
    ref: str
    created_at: datetime
    completed_at: datetime | None = None
    risk_category: str | None = None
    compliance_score: float | None = None
    finding_count: int | None = None
    error: str | None = None


_LOCK = asyncio.Lock()


def _supervisor():
    """Lazy access — orchestrator/main.py sets the global."""
    from src.api import main

    return main.supervisor


@router.post("", response_model=ScanSummary, status_code=202)
async def create_scan(
    req: ScanRequest,
    background: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ScanSummary:
    scan_id = f"scn_{uuid.uuid4().hex[:16]}"
    now = datetime.utcnow()
    state = {
        "scan_id": scan_id,
        "repo_url": str(req.repo_url),
        "ref": req.ref,
        "profile": None,
        "risk_posture": None,
        "finding_citations": [],
        "narrative": None,
        "final_report": None,
        "current_step": "queued",
        "workflow_status": "queued",
        "errors": [],
        "cost_tracking": {},
        "audit_log": [],
        "started_at": now.isoformat(),
        "completed_at": None,
    }
    repo = ScanRepository(db)
    await repo.create(state)

    background.add_task(
        _run_scan_task, scan_id, str(req.repo_url), req.ref, req.enrich_with_kg
    )

    return ScanSummary(
        scan_id=scan_id,
        status="queued",
        repo_url=str(req.repo_url),
        ref=req.ref,
        created_at=now,
    )


@router.get("", response_model=list[ScanSummary])
async def list_scans(
    status: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
) -> list[ScanSummary]:
    repo = ScanRepository(db)
    items = await repo.list_all(status=status, limit=limit)
    out: list[ScanSummary] = []
    for i in items:
        out.append(
            ScanSummary(
                scan_id=i["scan_id"],
                status=i.get("status") or "running",
                repo_url=i.get("repo_url", ""),
                ref=i.get("ref", "main"),
                created_at=_parse_dt(i.get("started_at")) or datetime.utcnow(),
                completed_at=_parse_dt(i.get("completed_at")),
                risk_category=i.get("risk_category"),
                finding_count=i.get("finding_count"),
            )
        )
    return out


@router.get("/{scan_id}")
async def get_scan(scan_id: str, db: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    repo = ScanRepository(db)
    state = await repo.get_state(scan_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return state


@router.get("/{scan_id}/findings")
async def get_findings(
    scan_id: str, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    repo = ScanRepository(db)
    state = await repo.get_state(scan_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    profile = state.get("profile") or {}
    return {
        "status": state.get("workflow_status"),
        "findings": profile.get("findings", []),
        "stats": profile.get("stats"),
    }


@router.get("/{scan_id}/report")
async def get_report(
    scan_id: str, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    repo = ScanRepository(db)
    state = await repo.get_state(scan_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    report = state.get("final_report")
    if not report:
        raise HTTPException(
            status_code=404,
            detail=f"Report not ready (status={state.get('workflow_status')})",
        )
    return report


async def _run_scan_task(
    scan_id: str, repo_url: str, ref: str, enrich_with_kg: bool
) -> None:
    """Background task: ingest → scan → supervisor → persist."""
    from src.database.session import AsyncSessionLocal
    import src.database.session as db_session

    db = None
    try:
        if db_session._db_available is not False:
            db = AsyncSessionLocal()
            db = await db.__aenter__()
    except Exception:
        db = None

    repo = ScanRepository(db)

    try:
        async with _LOCK:
            await repo.update(scan_id, {"workflow_status": "running", "current_step": "ingesting"})

        profile = await asyncio.to_thread(
            _sync_scan, scan_id, repo_url, ref
        )

        await repo.update(
            scan_id,
            {
                "profile": profile.model_dump(mode="json"),
                "current_step": "scanned",
            },
        )

        if enrich_with_kg and _supervisor() is not None:
            state = create_initial_state(
                scan_id=scan_id, repo_url=repo_url, ref=ref, profile=profile
            )
            final = await _supervisor().execute(state)
            await repo.update(
                scan_id,
                {
                    "risk_posture": final.get("risk_posture"),
                    "finding_citations": final.get("finding_citations") or [],
                    "narrative": final.get("narrative"),
                    "final_report": final.get("final_report"),
                    "cost_tracking": final.get("cost_tracking") or {},
                    "audit_log": final.get("audit_log") or [],
                    "workflow_status": final.get("workflow_status", "completed"),
                    "completed_at": final.get("completed_at") or datetime.utcnow().isoformat(),
                    "current_step": "completed",
                },
            )
        else:
            await repo.update(
                scan_id,
                {
                    "workflow_status": "completed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "current_step": "completed",
                },
            )

    except Exception as e:
        logger.exception("Scan %s failed: %s", scan_id, e)
        try:
            await repo.update(
                scan_id,
                {
                    "workflow_status": "failed",
                    "errors": [str(e)],
                    "completed_at": datetime.utcnow().isoformat(),
                },
            )
        except Exception:
            pass
    finally:
        if db is not None:
            try:
                await db.close()
            except Exception:
                pass


def _sync_scan(scan_id: str, repo_url: str, ref: str):
    """run_scan is async but uses gitpython which blocks; run on a fresh loop."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(
            run_scan(
                scan_id=scan_id,
                repo_url=repo_url,
                ref=ref,
                enrich_with_kg=False,  # KG enrichment is now done by the supervisor
            )
        )
    finally:
        loop.close()


def _parse_dt(v: Any) -> datetime | None:
    if v is None:
        return None
    if isinstance(v, datetime):
        return v
    try:
        return datetime.fromisoformat(str(v))
    except Exception:
        return None
