"""Base agent class for compliance agents."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from src.config import settings
from src.utils.logging import get_logger
from src.utils.cost_tracker import cost_tracker, estimate_cost
from src.state.compliance_state import ComplianceState, AuditLogEntry


class BaseAgent(ABC):
    """
    Base class for all compliance agents.

    Provides common functionality:
    - LLM initialization
    - Cost tracking
    - Audit logging
    - Error handling
    """

    def __init__(self, name: str, model: str | None = None):
        self.name = name
        self.model_name = model or settings.primary_model
        self.logger = get_logger(f"agent.{name}")

        # Initialize LLM
        self.llm = self._init_llm(self.model_name)

    def _init_llm(self, model: str) -> ChatGoogleGenerativeAI | ChatAnthropic:
        """Initialize the LLM based on model name."""
        if "claude" in model.lower():
            return ChatAnthropic(
                model=model,
                api_key=settings.anthropic_api_key,
                temperature=0.1,
            )
        else:
            # Use Gemini for all other models
            return ChatGoogleGenerativeAI(
                model=model,
                google_api_key=settings.gemini_api_key,
                temperature=0.1,
            )

    @abstractmethod
    async def execute(self, state: ComplianceState) -> dict[str, Any]:
        """
        Execute the agent's main task.

        Args:
            state: Current compliance state

        Returns:
            Dictionary with agent output to merge into state
        """
        pass

    async def invoke_llm(
        self,
        prompt: str,
        session_id: str | None = None,
    ) -> tuple[str, float]:
        """
        Invoke the LLM with cost tracking.

        Args:
            prompt: The prompt to send to the LLM
            session_id: Optional session ID for cost tracking

        Returns:
            Tuple of (response_text, cost_usd)
        """
        start_time = datetime.utcnow()

        # Check cost limits before proceeding
        estimated_cost = estimate_cost(prompt, "", self.model_name)
        can_proceed, reason = cost_tracker.can_proceed(estimated_cost, session_id)

        if not can_proceed:
            self.logger.warning(
                "Cost limit check failed",
                agent=self.name,
                reason=reason,
            )
            raise ValueError(f"Cost limit exceeded: {reason}")

        # Invoke LLM
        response = await self.llm.ainvoke(prompt)
        response_text = response.content

        # Calculate actual cost
        actual_cost = estimate_cost(prompt, response_text, self.model_name)
        cost_tracker.add_cost(self.name, actual_cost, session_id)

        duration = (datetime.utcnow() - start_time).total_seconds()

        self.logger.info(
            "LLM invocation complete",
            agent=self.name,
            model=self.model_name,
            cost_usd=actual_cost,
            duration_seconds=duration,
        )

        return response_text, actual_cost

    def create_audit_entry(
        self,
        action: str,
        input_summary: str | None = None,
        output_summary: str | None = None,
        cost_usd: float = 0.0,
        duration_seconds: float = 0.0,
    ) -> dict:
        """Create an audit log entry."""
        return AuditLogEntry(
            timestamp=datetime.utcnow(),
            agent=self.name,
            action=action,
            input_summary=input_summary,
            output_summary=output_summary,
            cost_usd=cost_usd,
            duration_seconds=duration_seconds,
        ).model_dump()

    def build_audit_update(
        self,
        state: ComplianceState,
        action: str,
        output: dict[str, Any],
        cost_usd: float = 0.0,
        duration_seconds: float = 0.0,
    ) -> dict[str, Any]:
        """Build partial state update with audit log entry and cost tracking.

        Returns a dict with 'audit_log' and 'cost_tracking' keys that
        LangGraph's reducers will merge into state (append for audit_log,
        additive merge for cost_tracking).
        """
        audit_entry = self.create_audit_entry(
            action=action,
            input_summary=state.get("system_description", "")[:100],
            output_summary=str(output)[:200],
            cost_usd=cost_usd,
            duration_seconds=duration_seconds,
        )
        return {
            "audit_log": [audit_entry],
            "cost_tracking": {self.name: cost_usd},
        }
