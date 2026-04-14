"""Base agent class — provides LLM handle, cost tracking, and audit helpers."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

from src.config import settings
from src.state.scan_state import ScanState
from src.utils.cost_tracker import cost_tracker, estimate_cost
from src.utils.logging import get_logger


class BaseAgent(ABC):
    def __init__(self, name: str, model: str | None = None):
        self.name = name
        self.model_name = model or settings.primary_model
        self.logger = get_logger(f"agent.{name}")
        self.llm = self._init_llm(self.model_name)

    def _init_llm(self, model: str):
        if "claude" in model.lower():
            return ChatAnthropic(
                model=model,
                api_key=settings.anthropic_api_key,
                temperature=0.1,
            )
        return ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.gemini_api_key,
            temperature=0.1,
        )

    @abstractmethod
    async def execute(self, state: ScanState) -> dict[str, Any]:
        """Return a partial state update."""

    async def invoke_llm(self, prompt: str, scan_id: str | None = None) -> tuple[str, float]:
        start = datetime.utcnow()
        est = estimate_cost(prompt, "", self.model_name)
        ok, reason = cost_tracker.can_proceed(est, scan_id)
        if not ok:
            self.logger.warning("Cost limit check failed", reason=reason)
            raise ValueError(f"Cost limit exceeded: {reason}")

        response = await self.llm.ainvoke(prompt)
        text = response.content if hasattr(response, "content") else str(response)
        actual = estimate_cost(prompt, text, self.model_name)
        cost_tracker.add_cost(self.name, actual, scan_id)

        self.logger.info(
            "LLM invocation complete",
            agent=self.name,
            model=self.model_name,
            cost_usd=actual,
            duration_seconds=(datetime.utcnow() - start).total_seconds(),
        )
        return text, actual

    def audit_update(
        self,
        action: str,
        summary: str,
        cost_usd: float = 0.0,
        duration_seconds: float = 0.0,
    ) -> dict[str, Any]:
        return {
            "audit_log": [
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "agent": self.name,
                    "action": action,
                    "output_summary": summary[:400],
                    "cost_usd": cost_usd,
                    "duration_seconds": duration_seconds,
                }
            ],
            "cost_tracking": {self.name: cost_usd},
        }
