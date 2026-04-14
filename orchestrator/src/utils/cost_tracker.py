"""Cost tracking for LLM API calls."""

from datetime import datetime, timedelta
from collections import defaultdict
from threading import Lock

import tiktoken


# Pricing per 1K tokens (as of Jan 2026, update as needed)
MODEL_PRICING = {
    # OpenAI
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    # Anthropic
    "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
    "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125},
    # Gemini
    "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
    "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
    "gemini-2.0-flash": {"input": 0.0001, "output": 0.0004},
    "gemini-2.5-flash": {"input": 0.00015, "output": 0.0006},
    "gemini-2.5-flash-lite": {"input": 0.000075, "output": 0.0003},
    # Embedding
    "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
}


def estimate_cost(
    input_text: str,
    output_text: str = "",
    model: str = "gpt-4o",
) -> float:
    """
    Estimate cost for an LLM API call.

    Args:
        input_text: Input/prompt text
        output_text: Generated output text
        model: Model name

    Returns:
        Estimated cost in USD
    """
    pricing = MODEL_PRICING.get(model, {"input": 0.01, "output": 0.03})

    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    input_tokens = len(encoding.encode(input_text))
    output_tokens = len(encoding.encode(output_text)) if output_text else 0

    input_cost = (input_tokens / 1000) * pricing["input"]
    output_cost = (output_tokens / 1000) * pricing["output"]

    return input_cost + output_cost


class CostTracker:
    """
    Track API costs across agents and sessions.

    Thread-safe cost tracking with daily and per-session limits.
    """

    def __init__(self, max_daily_spend: float = 50.0, max_session_spend: float = 5.0):
        self.max_daily_spend = max_daily_spend
        self.max_session_spend = max_session_spend

        self._daily_costs: dict[str, float] = defaultdict(float)
        self._session_costs: dict[str, float] = defaultdict(float)
        self._agent_costs: dict[str, float] = defaultdict(float)
        self._lock = Lock()

    def add_cost(self, agent_name: str, cost: float, session_id: str | None = None) -> None:
        """Record a cost for an agent."""
        with self._lock:
            today = datetime.now().strftime("%Y-%m-%d")
            self._daily_costs[today] += cost
            self._agent_costs[agent_name] += cost
            if session_id:
                self._session_costs[session_id] += cost

    def get_daily_spend(self) -> float:
        """Get total spend for today."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self._daily_costs.get(today, 0.0)

    def get_session_spend(self, session_id: str) -> float:
        """Get total spend for a session."""
        return self._session_costs.get(session_id, 0.0)

    def get_agent_spend(self, agent_name: str) -> float:
        """Get total spend for an agent."""
        return self._agent_costs.get(agent_name, 0.0)

    def can_proceed(self, estimated_cost: float, session_id: str | None = None) -> tuple[bool, str]:
        """
        Check if an action can proceed based on cost limits.

        Returns:
            Tuple of (can_proceed, reason)
        """
        daily_spend = self.get_daily_spend()

        if daily_spend + estimated_cost > self.max_daily_spend:
            return False, f"Daily limit exceeded: ${daily_spend:.2f} + ${estimated_cost:.2f} > ${self.max_daily_spend:.2f}"

        if session_id:
            session_spend = self.get_session_spend(session_id)
            if session_spend + estimated_cost > self.max_session_spend:
                return False, f"Session limit exceeded: ${session_spend:.2f} + ${estimated_cost:.2f} > ${self.max_session_spend:.2f}"

        return True, "OK"

    def get_statistics(self) -> dict:
        """Get cost statistics."""
        return {
            "daily_spend": self.get_daily_spend(),
            "daily_limit": self.max_daily_spend,
            "agent_costs": dict(self._agent_costs),
            "total_all_time": sum(self._daily_costs.values()),
        }

    def reset_daily(self) -> None:
        """Reset daily costs (for testing or manual reset)."""
        today = datetime.now().strftime("%Y-%m-%d")
        with self._lock:
            self._daily_costs[today] = 0.0


# Global cost tracker instance
cost_tracker = CostTracker()
