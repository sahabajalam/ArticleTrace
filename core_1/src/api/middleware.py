"""API middleware for monitoring and metrics."""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.monitoring.metrics import record_api_request


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to record API request metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and record metrics."""
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Calculate duration
        duration = time.time() - start_time

        # Extract endpoint path (normalize path parameters)
        path = request.url.path
        # Normalize paths with IDs to avoid high cardinality
        path_parts = path.split("/")
        normalized_parts = []
        for i, part in enumerate(path_parts):
            # Check if this looks like an ID (UUID, numeric, etc.)
            if self._is_id_like(part) and i > 0:
                normalized_parts.append("{id}")
            else:
                normalized_parts.append(part)
        normalized_path = "/".join(normalized_parts)

        # Record metrics (skip /metrics endpoint to avoid recursion)
        if not path.startswith("/metrics"):
            record_api_request(
                method=request.method,
                endpoint=normalized_path,
                status_code=response.status_code,
                duration=duration,
            )

        return response

    def _is_id_like(self, value: str) -> bool:
        """Check if a value looks like an ID."""
        if not value:
            return False

        # UUID pattern
        if len(value) == 36 and value.count("-") == 4:
            return True

        # Numeric ID
        if value.isdigit():
            return True

        # Alphanumeric ID (common pattern)
        if len(value) >= 8 and value.replace("-", "").replace("_", "").isalnum():
            return True

        return False
