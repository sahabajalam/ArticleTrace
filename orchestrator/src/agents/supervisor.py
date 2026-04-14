"""Supervisor — orchestrates the scan-driven compliance workflow.

Graph:
  classify_risk → research_legal → generate_narrative → synthesize → END

No HITL branch: static scanners produce deterministic, auditable evidence, so
there is no classification-uncertainty branch to pause on.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from langgraph.graph import StateGraph, END

from src.agents.documentation_generator import DocumentationGeneratorAgent
from src.agents.legal_research import LegalResearchAgent
from src.agents.risk_classifier import RiskClassifierAgent
from src.state.scan_state import ScanState
from src.utils.logging import get_logger

logger = get_logger(__name__)


class SupervisorAgent:
    def __init__(self):
        self.risk_classifier = RiskClassifierAgent()
        self.legal_research = LegalResearchAgent()
        self.documentation_generator = DocumentationGeneratorAgent()
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ScanState)
        graph.add_node("classify_risk", self._classify_risk)
        graph.add_node("research_legal", self._research_legal)
        graph.add_node("generate_narrative", self._generate_narrative)
        graph.add_node("synthesize", self._synthesize)

        graph.set_entry_point("classify_risk")
        graph.add_edge("classify_risk", "research_legal")
        graph.add_edge("research_legal", "generate_narrative")
        graph.add_edge("generate_narrative", "synthesize")
        graph.add_edge("synthesize", END)
        return graph.compile()

    async def execute(self, state: ScanState) -> dict[str, Any]:
        scan_id = state.get("scan_id", "default")
        logger.info("Supervisor starting", scan_id=scan_id)
        try:
            final = await self.workflow.ainvoke(state)
            final["workflow_status"] = "completed"
            final["completed_at"] = datetime.utcnow().isoformat()
            logger.info(
                "Supervisor finished",
                scan_id=scan_id,
                total_cost=sum(final.get("cost_tracking", {}).values()),
            )
            return final
        except Exception as e:
            logger.error("Supervisor failed", scan_id=scan_id, error=str(e))
            return {
                **state,
                "workflow_status": "failed",
                "errors": state.get("errors", []) + [str(e)],
                "completed_at": datetime.utcnow().isoformat(),
            }

    async def close(self) -> None:
        return None

    async def _classify_risk(self, state: ScanState) -> dict[str, Any]:
        logger.info("Classifying risk", scan_id=state.get("scan_id"))
        return await self.risk_classifier.execute(state)

    async def _research_legal(self, state: ScanState) -> dict[str, Any]:
        logger.info("Researching legal anchors", scan_id=state.get("scan_id"))
        return await self.legal_research.execute(state)

    async def _generate_narrative(self, state: ScanState) -> dict[str, Any]:
        logger.info("Generating narrative", scan_id=state.get("scan_id"))
        return await self.documentation_generator.execute(state)

    async def _synthesize(self, state: ScanState) -> dict[str, Any]:
        profile = state.get("profile") or {}
        posture = state.get("risk_posture") or {}
        narrative = state.get("narrative") or {}
        citations = state.get("finding_citations") or []

        final_report = {
            "scan_id": state.get("scan_id"),
            "repo_url": state.get("repo_url"),
            "ref": state.get("ref"),
            "risk_posture": posture,
            "profile": profile,
            "finding_citations": citations,
            "narrative": narrative,
            "completed_at": datetime.utcnow().isoformat(),
            "cost_tracking": state.get("cost_tracking", {}),
        }
        return {
            "final_report": final_report,
            "current_step": "completed",
        }
