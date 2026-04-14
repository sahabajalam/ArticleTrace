"""Error handling utilities for agents."""

from functools import wraps
from typing import Any, Callable, TypeVar
import traceback

from src.utils.logging import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class AgentError(Exception):
    """Base exception for agent errors."""

    def __init__(self, agent_name: str, message: str, details: dict | None = None):
        self.agent_name = agent_name
        self.message = message
        self.details = details or {}
        super().__init__(f"[{agent_name}] {message}")


class RateLimitError(AgentError):
    """Raised when rate limit is exceeded."""
    pass


class CostLimitError(AgentError):
    """Raised when cost limit is exceeded."""
    pass


class HumanApprovalRequired(AgentError):
    """Raised when human approval is needed."""

    def __init__(self, agent_name: str, reason: str, action: dict):
        super().__init__(agent_name, f"Human approval required: {reason}")
        self.reason = reason
        self.action = action


class GraphRAGError(AgentError):
    """Raised when GraphRAG API fails."""
    pass


def safe_execute(
    default_return: T | None = None,
    exceptions: tuple = (Exception,),
    log_error: bool = True,
) -> Callable:
    """
    Decorator for safe function execution with fallback.

    Args:
        default_return: Value to return on failure
        exceptions: Tuple of exceptions to catch
        log_error: Whether to log errors

    Returns:
        Decorated function
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T | None]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T | None:
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                if log_error:
                    logger.error(
                        "Function execution failed",
                        function=func.__name__,
                        error=str(e),
                        traceback=traceback.format_exc(),
                    )
                return default_return

        return wrapper

    return decorator


def safe_execute_async(
    default_return: T | None = None,
    exceptions: tuple = (Exception,),
    log_error: bool = True,
) -> Callable:
    """
    Async decorator for safe function execution with fallback.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T | None:
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                if log_error:
                    logger.error(
                        "Async function execution failed",
                        function=func.__name__,
                        error=str(e),
                        traceback=traceback.format_exc(),
                    )
                return default_return

        return wrapper

    return decorator
