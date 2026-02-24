"""Rate limiting configuration using slowapi."""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

from src.config import get_settings


settings = get_settings()


def get_client_ip(request: Request) -> str:
    """Get client IP for rate limiting.

    Handles X-Forwarded-For header for reverse proxy setups.
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # Get the first IP in the chain (original client)
        return forwarded_for.split(",")[0].strip()
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(
    key_func=get_client_ip,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"],
)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": f"Too many requests. Limit: {exc.detail}",
            "retry_after": getattr(exc, "retry_after", 60),
        },
        headers={
            "Retry-After": str(getattr(exc, "retry_after", 60)),
            "X-RateLimit-Limit": str(settings.rate_limit_per_minute),
        },
    )


# Rate limit decorators for different endpoint types
def rate_limit_standard():
    """Standard rate limit for most endpoints."""
    return limiter.limit(f"{settings.rate_limit_per_minute}/minute")


def rate_limit_strict():
    """Stricter rate limit for sensitive endpoints."""
    return limiter.limit(f"{settings.rate_limit_per_minute // 2}/minute")


def rate_limit_relaxed():
    """Relaxed rate limit for health checks and metrics."""
    return limiter.limit(f"{settings.rate_limit_per_minute * 2}/minute")
