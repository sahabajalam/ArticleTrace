"""Supervisor Agent with LangGraph workflow orchestration."""

from datetime import datetime
from typing import Any, Literal

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.agents.base import BaseAgent
from src.agents.risk_classifier import RiskClassifierAgent
from src.agents.technical_assessor import TechnicalAssessorAgent
from src.agents.legal_research import LegalResearchAgent
from src.agents.documentation_generator import DocumentationGeneratorAgent
from src.config import settings
from src.state.compliance_state import ComplianceState, RiskCategory
from src.utils.logging import get_logger

logger = get_logger(__name__)


class SupervisorAgent(BaseAgent):
    """
    Supervisor Agent that orchestrates the compliance workflow.

    Responsibilities:
    - Receives compliance assessment requests
    - Decomposes into sub-tasks
    - Routes to specialist agents
    - Resolves conflicts between agents
    - Synthesizes final compliance report
    """

    def __init__(self):
        super().__init__(
            name="supervisor",
            model=settings.primary_model,
        )

        # Initialize specialist agents
        self.risk_classifier = RiskClassifierAgent()
        self.technical_assessor = TechnicalAssessorAgent()
        self.legal_research = LegalResearchAgent()
        self.documentation_generator = DocumentationGeneratorAgent()

        # Checkpointer enables workflow pause/resume for human-in-the-loop
        self.checkpointer = MemorySaver()

        # Build the workflow
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Build the LangGraph workflow with checkpointing and interrupt support.

        Graph topology:
          classify_risk → check_human_review → [conditional]
                                                 ├─ needs_review → await_approval → assess_gdpr
                                                 └─ proceed → assess_gdpr
          assess_gdpr → research_legal → check_conflicts → generate_docs → synthesize → END

        The await_approval node uses interrupt_before so that LangGraph pauses
        the workflow before executing it. The API can then resume the workflow
        after human approval by calling workflow.ainvoke(None, config) again.
        """
        workflow = StateGraph(ComplianceState)

        # Add nodes for each agent
        workflow.add_node("classify_risk", self._classify_risk)
        workflow.add_node("check_human_review", self._check_human_review)
        workflow.add_node("await_approval", self._await_approval)
        workflow.add_node("assess_gdpr", self._assess_gdpr)
        workflow.add_node("research_legal", self._research_legal)
        workflow.add_node("check_conflicts", self._check_conflicts)
        workflow.add_node("generate_docs", self._generate_docs)
        workflow.add_node("synthesize", self._synthesize_report)

        # Set entry point
        workflow.set_entry_point("classify_risk")

        # Add edges
        workflow.add_edge("classify_risk", "check_human_review")

        # Conditional edge: human review needed?
        workflow.add_conditional_edges(
            "check_human_review",
            self._route_after_classification,
            {
                "needs_review": "await_approval",
                "proceed": "assess_gdpr",
            },
        )

        # After approval, continue with assessment
        workflow.add_edge("await_approval", "assess_gdpr")

        # GDPR assessment leads to legal research
        workflow.add_edge("assess_gdpr", "research_legal")

        # Check for conflicts after assessments
        workflow.add_edge("research_legal", "check_conflicts")

        # After conflict check, generate docs
        workflow.add_edge("check_conflicts", "generate_docs")

        # Documentation leads to final synthesis
        workflow.add_edge("generate_docs", "synthesize")

        # End after synthesis
        workflow.add_edge("synthesize", END)

        return workflow.compile(
            checkpointer=self.checkpointer,
            interrupt_before=["await_approval"],
        )

    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Execute the full compliance workflow.

        This is the main entry point for running an assessment.
        The checkpointer uses session_id as the thread_id so that
        paused workflows can be resumed later via resume().
        """
        session_id = state.get("session_id", "default")

        logger.info(
            "Starting compliance assessment",
            session_id=session_id,
            system_type=state.get("system_type"),
        )

        start_time = datetime.utcnow()
        config = {"configurable": {"thread_id": session_id}}

        try:
            # Run the workflow — will pause at interrupt_before nodes
            final_state = await self.workflow.ainvoke(state, config)

            # Check if the workflow paused at an interrupt
            graph_state = await self.workflow.aget_state(config)
            if graph_state.next:
                # Workflow is paused (e.g., awaiting human approval)
                logger.info(
                    "Workflow paused for human review",
                    session_id=session_id,
                    paused_before=graph_state.next,
                )
                final_state["workflow_status"] = "awaiting_approval"
                return final_state

            final_state["workflow_status"] = "completed"
            final_state["completed_at"] = datetime.utcnow().isoformat()

            duration = (datetime.utcnow() - start_time).total_seconds()

            logger.info(
                "Compliance assessment complete",
                session_id=session_id,
                duration_seconds=duration,
                total_cost=sum(final_state.get("cost_tracking", {}).values()),
            )

            return final_state

        except Exception as e:
            logger.error(
                "Compliance assessment failed",
                session_id=session_id,
                error=str(e),
            )
            return {
                **state,
                "workflow_status": "failed",
                "errors": state.get("errors", []) + [str(e)],
            }

    async def resume(self, session_id: str, human_decision: str = "approved") -> dict[str, Any]:
        """
        Resume a paused workflow after human approval.

        Args:
            session_id: The session_id of the paused assessment
            human_decision: "approved" or "rejected"

        Returns:
            Final state after workflow completion
        """
        config = {"configurable": {"thread_id": session_id}}

        logger.info(
            "Resuming workflow after human decision",
            session_id=session_id,
            decision=human_decision,
        )

        # Update the state with the human decision before resuming
        await self.workflow.aupdate_state(
            config,
            {
                "human_decision": human_decision,
                "requires_human_review": False,
                "workflow_status": "running",
                "audit_log": [{
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": "supervisor",
                    "action": "human_decision",
                    "input_summary": f"Decision: {human_decision}",
                    "output_summary": f"Human {human_decision} the assessment",
                    "human_approved": human_decision == "approved",
                }],
            },
        )

        if human_decision == "rejected":
            # Skip the await_approval node and go straight to END
            current_state = await self.workflow.aget_state(config)
            state = current_state.values
            state["workflow_status"] = "rejected"
            return state

        # Resume execution — LangGraph continues from the interrupt point
        final_state = await self.workflow.ainvoke(None, config)

        graph_state = await self.workflow.aget_state(config)
        if not graph_state.next:
            final_state["workflow_status"] = "completed"
            final_state["completed_at"] = datetime.utcnow().isoformat()

        return final_state

    async def _classify_risk(self, state: ComplianceState) -> dict[str, Any]:
        """Run risk classification. Returns partial state update."""
        logger.info("Running risk classification", session_id=state.get("session_id"))
        return await self.risk_classifier.execute(state)

    def _route_after_classification(
        self,
        state: ComplianceState,
    ) -> Literal["needs_review", "proceed"]:
        """Determine routing after risk classification."""
        if state.get("requires_human_review", False):
            return "needs_review"
        return "proceed"

    async def _check_human_review(self, state: ComplianceState) -> dict[str, Any]:
        """Check if human review is needed based on risk classification.

        Returns partial state update with review flags.
        """
        risk = state.get("risk_classification", {})
        update: dict[str, Any] = {}

        # Rule 1: Prohibited systems ALWAYS require human review
        if risk.get("category") == RiskCategory.PROHIBITED.value:
            update["requires_human_review"] = True
            update["workflow_status"] = "awaiting_approval"
            logger.info(
                "Human review required: Prohibited system detected",
                session_id=state.get("session_id"),
            )

        # Rule 2: High-risk with low confidence
        elif (
            risk.get("category") == RiskCategory.HIGH_RISK.value
            and risk.get("confidence", 1.0) < 0.80
        ):
            update["requires_human_review"] = True
            update["workflow_status"] = "awaiting_approval"
            logger.info(
                "Human review required: Low confidence on high-risk classification",
                session_id=state.get("session_id"),
                confidence=risk.get("confidence"),
            )

        return update

    async def _await_approval(self, state: ComplianceState) -> dict[str, Any]:
        """
        Wait for human approval.

        With checkpointing enabled, LangGraph's interrupt_before mechanism
        pauses the workflow here. The API resumes it after human approval.
        When no checkpointer is configured, auto-approves for demonstration.
        """
        logger.info(
            "Awaiting human approval",
            session_id=state.get("session_id"),
            risk_category=state.get("risk_classification", {}).get("category"),
        )

        return {
            "human_decision": "auto_approved_for_demo",
            "requires_human_review": False,
            "workflow_status": "running",
            "audit_log": [{
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "supervisor",
                "action": "human_approval_required",
                "input_summary": f"Risk: {state.get('risk_classification', {}).get('category')}",
                "output_summary": "Auto-approved for demonstration",
                "human_approved": True,
            }],
        }

    async def _assess_gdpr(self, state: ComplianceState) -> dict[str, Any]:
        """Run GDPR assessment. Returns partial state update."""
        logger.info("Running GDPR assessment", session_id=state.get("session_id"))
        return await self.technical_assessor.execute(state)

    async def _research_legal(self, state: ComplianceState) -> dict[str, Any]:
        """Run legal research. Returns partial state update."""
        logger.info("Running legal research", session_id=state.get("session_id"))
        return await self.legal_research.execute(state)

    async def _check_conflicts(self, state: ComplianceState) -> dict[str, Any]:
        """Check for conflicts between agent outputs. Returns partial state update."""
        conflicts = self._detect_conflicts(state)

        if conflicts:
            logger.warning(
                "Conflicts detected between agents",
                session_id=state.get("session_id"),
                conflicts=conflicts,
            )
            # Return conflicts via errors reducer (operator.add appends)
            return {"errors": conflicts}

        return {}

    def _detect_conflicts(self, state: ComplianceState) -> list[str]:
        """
        Detect conflicts between agent outputs.

        Examples:
        - Risk Classifier says HIGH_RISK but Technical Assessor finds no issues
        - Legal Research can't find citations for the classification
        """
        conflicts = []

        risk = state.get("risk_classification", {})
        gdpr = state.get("gdpr_audit", {})
        legal = state.get("legal_citations", {})

        # Conflict 1: High-risk but no GDPR violations (unusual)
        if (
            risk.get("category") == RiskCategory.HIGH_RISK.value
            and gdpr.get("gdpr_compliant", False)
            and not gdpr.get("warnings")
        ):
            conflicts.append(
                "Conflict: High-risk classification but no GDPR concerns identified. "
                "Manual review recommended."
            )

        # Conflict 2: Low confidence in legal research
        if legal.get("confidence", 1.0) < 0.5:
            conflicts.append(
                "Warning: Low confidence in legal citations. "
                "Results may be incomplete."
            )

        # Conflict 3: GDPR violations but classified as minimal risk
        if (
            risk.get("category") == RiskCategory.MINIMAL_RISK.value
            and gdpr.get("violations")
        ):
            conflicts.append(
                "Conflict: Minimal risk classification but GDPR violations detected. "
                "Consider re-evaluation."
            )

        return conflicts

    async def _generate_docs(self, state: ComplianceState) -> dict[str, Any]:
        """Generate compliance documentation. Returns partial state update."""
        logger.info("Generating compliance documentation", session_id=state.get("session_id"))
        return await self.documentation_generator.execute(state)

    async def _synthesize_report(self, state: ComplianceState) -> dict[str, Any]:
        """Synthesize final compliance report. Returns partial state update."""
        logger.info("Synthesizing final report", session_id=state.get("session_id"))

        risk = state.get("risk_classification", {})
        gdpr = state.get("gdpr_audit", {})
        legal = state.get("legal_citations", {})
        docs = state.get("compliance_docs", {})

        # Calculate overall compliance score
        compliance_score = self._calculate_compliance_score(risk, gdpr, legal)

        # Generate executive summary
        summary = self._generate_executive_summary(state, compliance_score)

        # Create final report structure
        final_report = {
            "executive_summary": summary,
            "compliance_score": compliance_score,
            "risk_classification": risk,
            "gdpr_compliance": {
                "compliant": gdpr.get("gdpr_compliant", False),
                "violation_count": len(gdpr.get("violations", [])),
                "warning_count": len(gdpr.get("warnings", [])),
                "dpia_required": gdpr.get("dpia_required", False),
            },
            "legal_basis": {
                "citations_found": len(legal.get("relevant_articles", [])),
                "confidence": legal.get("confidence", 0),
            },
            "documents_generated": docs.get("generated_count", 0),
            "recommendations": self._compile_recommendations(state),
            "next_steps": self._determine_next_steps(state),
            "cost_summary": state.get("cost_tracking", {}),
            "assessment_metadata": {
                "session_id": state.get("session_id"),
                "started_at": state.get("started_at"),
                "completed_at": datetime.utcnow().isoformat(),
                "agents_involved": ["risk_classifier", "technical_assessor", "legal_research", "documentation_generator"],
            },
        }

        return {
            "final_report": final_report,
            "current_step": "completed",
        }

    def _calculate_compliance_score(
        self,
        risk: dict[str, Any],
        gdpr: dict[str, Any],
        legal: dict[str, Any],
    ) -> float:
        """Calculate overall compliance score (0-100)."""
        score = 100.0

        # Deduct for risk category
        category = risk.get("category", "")
        if category == RiskCategory.PROHIBITED.value:
            score -= 50
        elif category == RiskCategory.HIGH_RISK.value:
            score -= 20

        # Deduct for GDPR violations
        violations = gdpr.get("violations", [])
        score -= len(violations) * 10

        # Deduct for GDPR warnings
        warnings = gdpr.get("warnings", [])
        score -= len(warnings) * 5

        # Add points for having legal citations
        if legal.get("relevant_articles"):
            score += 5  # Shows due diligence

        return max(0, min(100, score))

    def _generate_executive_summary(
        self,
        state: ComplianceState,
        compliance_score: float,
    ) -> str:
        """Generate executive summary."""
        risk = state.get("risk_classification", {})
        gdpr = state.get("gdpr_audit", {})

        category = risk.get("category", "UNKNOWN")
        violations = len(gdpr.get("violations", []))

        if category == RiskCategory.PROHIBITED.value:
            return (
                f"CRITICAL: This AI system is classified as PROHIBITED under EU AI Act Article 5. "
                f"Deployment is legally forbidden. Immediate review and system redesign required."
            )
        elif category == RiskCategory.HIGH_RISK.value:
            return (
                f"This AI system is classified as HIGH-RISK under EU AI Act {risk.get('annex', 'Annex III')}. "
                f"Conformity assessment is MANDATORY before deployment. "
                f"GDPR audit found {violations} violation(s). "
                f"Compliance score: {compliance_score:.0f}/100."
            )
        elif violations > 0:
            return (
                f"This AI system is classified as {category} under EU AI Act. "
                f"However, GDPR audit identified {violations} violation(s) requiring remediation. "
                f"Compliance score: {compliance_score:.0f}/100."
            )
        else:
            return (
                f"This AI system is classified as {category} under EU AI Act. "
                f"GDPR compliance verified with no violations. "
                f"Compliance score: {compliance_score:.0f}/100."
            )

    def _compile_recommendations(self, state: ComplianceState) -> list[str]:
        """Compile all recommendations from agents."""
        recommendations = []

        # From risk classification
        risk = state.get("risk_classification", {})
        recommendations.extend(risk.get("requirements", []))

        # From GDPR audit
        gdpr = state.get("gdpr_audit", {})
        recommendations.extend(gdpr.get("recommendations", []))

        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recommendations.append(rec)

        return unique_recommendations

    def _determine_next_steps(self, state: ComplianceState) -> list[str]:
        """Determine next steps based on assessment results."""
        next_steps = []

        risk = state.get("risk_classification", {})
        gdpr = state.get("gdpr_audit", {})

        category = risk.get("category", "")

        if category == RiskCategory.PROHIBITED.value:
            next_steps.extend([
                "DO NOT DEPLOY this system in its current form",
                "Consult with legal team for system redesign options",
                "Consider alternative approaches that comply with EU AI Act",
            ])
        elif category == RiskCategory.HIGH_RISK.value:
            next_steps.extend([
                "Complete Conformity Assessment documentation",
                "Register system in EU AI Act database",
                "Implement required human oversight measures",
                "Obtain CE marking before deployment",
            ])

        if gdpr.get("dpia_required"):
            next_steps.append("Complete and document full DPIA")
            next_steps.append("Consult with Data Protection Officer")

        if gdpr.get("violations"):
            next_steps.append("Address all GDPR violations before deployment")

        if not next_steps:
            next_steps.append("System may proceed to deployment with standard monitoring")

        return next_steps

    async def close(self):
        """Clean up resources."""
        await self.legal_research.close()
