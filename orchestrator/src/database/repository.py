"""Repository for scan persistence.

Falls back to in-memory storage when the database is unavailable.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ScanModel


_memory_store: dict[str, dict[str, Any]] = {}


class ScanRepository:
    def __init__(self, db: AsyncSession | None):
        self.db = db
        self._use_memory = db is None

    async def create(self, state: dict[str, Any]) -> Any:
        if self._use_memory:
            _memory_store[state["scan_id"]] = dict(state)
            return state
        model = ScanModel.from_state_dict(state)
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def _get(self, scan_id: str) -> Any | None:
        if self._use_memory:
            return _memory_store.get(scan_id)
        result = await self.db.execute(
            select(ScanModel).where(ScanModel.scan_id == scan_id)
        )
        return result.scalar_one_or_none()

    async def get_state(self, scan_id: str) -> dict[str, Any] | None:
        if self._use_memory:
            return _memory_store.get(scan_id)
        model = await self._get(scan_id)
        return model.to_state_dict() if model else None

    async def update(self, scan_id: str, state: dict[str, Any]) -> Any | None:
        if self._use_memory:
            if scan_id in _memory_store:
                _memory_store[scan_id].update(state)
                return _memory_store[scan_id]
            return None
        model = await self._get(scan_id)
        if not model:
            return None
        model.update_from_state(state)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def list_all(
        self,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        if self._use_memory:
            items = list(_memory_store.values())
            if status:
                items = [i for i in items if i.get("workflow_status") == status]
            items.sort(key=lambda x: x.get("started_at", ""), reverse=True)
            return [_summary(i) for i in items[:limit]]

        query = select(ScanModel)
        if status:
            query = query.where(ScanModel.workflow_status == status)
        query = query.order_by(ScanModel.started_at.desc()).limit(limit)
        result = await self.db.execute(query)
        models = result.scalars().all()
        return [_summary(m.to_state_dict()) for m in models]

    async def count_by_status(self) -> dict[str, int]:
        if self._use_memory:
            counts: dict[str, int] = {}
            for item in _memory_store.values():
                s = item.get("workflow_status", "unknown")
                counts[s] = counts.get(s, 0) + 1
            return counts
        result = await self.db.execute(select(ScanModel))
        counts: dict[str, int] = {}
        for m in result.scalars().all():
            s = m.workflow_status or "unknown"
            counts[s] = counts.get(s, 0) + 1
        return counts


def _summary(state: dict[str, Any]) -> dict[str, Any]:
    posture = state.get("risk_posture") or {}
    profile = state.get("profile") or {}
    stats = profile.get("stats") if isinstance(profile, dict) else None
    return {
        "scan_id": state.get("scan_id"),
        "repo_url": state.get("repo_url"),
        "ref": state.get("ref"),
        "status": state.get("workflow_status"),
        "risk_category": posture.get("category"),
        "finding_count": (stats or {}).get("total_findings", 0) if stats else None,
        "started_at": state.get("started_at"),
        "completed_at": state.get("completed_at"),
    }
