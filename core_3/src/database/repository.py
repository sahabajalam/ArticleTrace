"""Repository for assessment CRUD operations."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AssessmentModel
from src.state.compliance_state import ComplianceState


class AssessmentRepository:
    """Repository for assessment database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, state: ComplianceState) -> AssessmentModel:
        """Create a new assessment."""
        assessment = AssessmentModel.from_state_dict(state)
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def get(self, session_id: str) -> AssessmentModel | None:
        """Get assessment by session ID."""
        result = await self.db.execute(
            select(AssessmentModel).where(AssessmentModel.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def get_state(self, session_id: str) -> ComplianceState | None:
        """Get assessment as ComplianceState dict."""
        assessment = await self.get(session_id)
        if assessment:
            return assessment.to_state_dict()
        return None

    async def update(self, session_id: str, state: dict[str, Any]) -> AssessmentModel | None:
        """Update an existing assessment."""
        assessment = await self.get(session_id)
        if not assessment:
            return None

        assessment.update_from_state(state)
        await self.db.commit()
        await self.db.refresh(assessment)
        return assessment

    async def list_all(
        self,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List assessments with optional filtering."""
        query = select(AssessmentModel)

        if status:
            query = query.where(AssessmentModel.workflow_status == status)

        query = query.order_by(AssessmentModel.started_at.desc()).limit(limit)

        result = await self.db.execute(query)
        assessments = result.scalars().all()

        return [
            {
                "session_id": a.session_id,
                "status": a.workflow_status,
                "system_type": a.system_type,
                "started_at": a.started_at.isoformat() if a.started_at else None,
                "completed_at": a.completed_at.isoformat() if a.completed_at else None,
                "risk_category": a.risk_classification.get("category") if a.risk_classification else None,
            }
            for a in assessments
        ]

    async def delete(self, session_id: str) -> bool:
        """Delete an assessment."""
        assessment = await self.get(session_id)
        if not assessment:
            return False

        await self.db.delete(assessment)
        await self.db.commit()
        return True

    async def count_by_status(self) -> dict[str, int]:
        """Count assessments grouped by status."""
        result = await self.db.execute(select(AssessmentModel))
        assessments = result.scalars().all()

        counts: dict[str, int] = {}
        for a in assessments:
            status = a.workflow_status or "unknown"
            counts[status] = counts.get(status, 0) + 1

        return counts
