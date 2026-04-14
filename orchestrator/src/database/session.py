"""Database session management."""

import ssl
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


def get_async_database_url() -> str:
    """Convert database URL to async format."""
    url = settings.database_url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def _build_connect_args() -> dict:
    """Build connect_args for asyncpg, adding SSL for cloud providers."""
    url = settings.database_url
    connect_args: dict = {}

    # Supabase / cloud PostgreSQL: enable SSL + disable prepared statements
    # (transaction pooler doesn't support prepared statements)
    if "supabase" in url or "neon.tech" in url or "aivencloud" in url:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        connect_args["ssl"] = ssl_ctx
        connect_args["statement_cache_size"] = 0

    return connect_args


engine = create_async_engine(
    get_async_database_url(),
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    connect_args=_build_connect_args(),
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Track whether the DB has been confirmed reachable
_db_available: bool | None = None  # None = not yet tested


async def init_db() -> None:
    """Initialize database tables. Sets _db_available flag."""
    global _db_available
    try:
        async with engine.begin() as conn:
            from src.database.models import Base
            await conn.run_sync(Base.metadata.create_all)
        _db_available = True
    except Exception as e:
        _db_available = False
        raise


async def get_db() -> AsyncGenerator[AsyncSession | None, None]:
    """Dependency for getting database session. Yields None if DB unavailable."""
    global _db_available

    # If we already know DB is down, skip immediately
    if _db_available is False:
        yield None
        return

    # Try to provide a real session
    try:
        async with AsyncSessionLocal() as session:
            # Quick connectivity test on first use or if status unknown
            if _db_available is None:
                await session.execute(text("SELECT 1"))
                _db_available = True

            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    except Exception as e:
        _db_available = False
        logger.warning(f"Database unavailable, using in-memory fallback: {e}")
        yield None
