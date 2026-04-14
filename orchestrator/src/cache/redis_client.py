"""Redis client for session state caching."""

import json
from typing import Any

import redis.asyncio as redis

from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class RedisClient:
    """Async Redis client for session state management."""

    def __init__(self, url: str | None = None):
        self.url = url or settings.redis_url
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            self._client = redis.from_url(
                self.url,
                encoding="utf-8",
                decode_responses=True,
            )
            await self._client.ping()
            logger.info("Connected to Redis", url=self.url.split("@")[-1])
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {e}")
            self._client = None

    async def close(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()
            logger.info("Redis connection closed")

    @property
    def is_connected(self) -> bool:
        """Check if Redis is connected."""
        return self._client is not None

    async def set_session_state(
        self,
        session_id: str,
        state: dict[str, Any],
        ttl_seconds: int = 3600 * 24,  # 24 hours default
    ) -> bool:
        """Store session state in Redis."""
        if not self._client:
            return False

        try:
            key = f"session:{session_id}"
            await self._client.setex(
                key,
                ttl_seconds,
                json.dumps(state, default=str),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to set session state: {e}")
            return False

    async def get_session_state(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve session state from Redis."""
        if not self._client:
            return None

        try:
            key = f"session:{session_id}"
            data = await self._client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get session state: {e}")
            return None

    async def update_session_state(
        self,
        session_id: str,
        updates: dict[str, Any],
        ttl_seconds: int = 3600 * 24,
    ) -> bool:
        """Update specific fields in session state."""
        if not self._client:
            return False

        try:
            current_state = await self.get_session_state(session_id)
            if current_state is None:
                current_state = {}

            current_state.update(updates)
            return await self.set_session_state(session_id, current_state, ttl_seconds)
        except Exception as e:
            logger.error(f"Failed to update session state: {e}")
            return False

    async def delete_session_state(self, session_id: str) -> bool:
        """Delete session state from Redis."""
        if not self._client:
            return False

        try:
            key = f"session:{session_id}"
            await self._client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Failed to delete session state: {e}")
            return False

    async def set_workflow_status(
        self,
        session_id: str,
        status: str,
        ttl_seconds: int = 3600,
    ) -> bool:
        """Set workflow status for a session."""
        if not self._client:
            return False

        try:
            key = f"workflow:{session_id}:status"
            await self._client.setex(key, ttl_seconds, status)
            return True
        except Exception as e:
            logger.error(f"Failed to set workflow status: {e}")
            return False

    async def get_workflow_status(self, session_id: str) -> str | None:
        """Get workflow status for a session."""
        if not self._client:
            return None

        try:
            key = f"workflow:{session_id}:status"
            return await self._client.get(key)
        except Exception as e:
            logger.error(f"Failed to get workflow status: {e}")
            return None

    async def cache_agent_result(
        self,
        session_id: str,
        agent_name: str,
        result: dict[str, Any],
        ttl_seconds: int = 3600,
    ) -> bool:
        """Cache agent result for a session."""
        if not self._client:
            return False

        try:
            key = f"agent:{session_id}:{agent_name}"
            await self._client.setex(
                key,
                ttl_seconds,
                json.dumps(result, default=str),
            )
            return True
        except Exception as e:
            logger.error(f"Failed to cache agent result: {e}")
            return False

    async def get_agent_result(
        self,
        session_id: str,
        agent_name: str,
    ) -> dict[str, Any] | None:
        """Get cached agent result."""
        if not self._client:
            return None

        try:
            key = f"agent:{session_id}:{agent_name}"
            data = await self._client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Failed to get agent result: {e}")
            return None

    async def increment_counter(
        self,
        key: str,
        ttl_seconds: int | None = None,
    ) -> int:
        """Increment a counter in Redis."""
        if not self._client:
            return 0

        try:
            value = await self._client.incr(key)
            if ttl_seconds:
                await self._client.expire(key, ttl_seconds)
            return value
        except Exception as e:
            logger.error(f"Failed to increment counter: {e}")
            return 0

    async def get_counter(self, key: str) -> int:
        """Get counter value."""
        if not self._client:
            return 0

        try:
            value = await self._client.get(key)
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"Failed to get counter: {e}")
            return 0


# Global Redis client instance
_redis_client: RedisClient | None = None


async def get_redis_client() -> RedisClient:
    """Get or create Redis client instance."""
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
        await _redis_client.connect()
    return _redis_client


async def close_redis_client() -> None:
    """Close global Redis client."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
