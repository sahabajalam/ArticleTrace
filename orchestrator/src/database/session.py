"""Database session management."""

import ssl
from typing import AsyncGenerator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


# Hosts whose connection poolers run PgBouncer in transaction mode, where
# asyncpg's prepared statements are not supported, and which always require TLS.
_MANAGED_HOSTS = ("neon.tech", "supabase", "aivencloud")

# libpq understands these; asyncpg's connect() does not, and SQLAlchemy forwards
# unknown query parameters straight through as keyword arguments. Neon hands out
# URLs ending `?sslmode=require&channel_binding=require`, which raised
#     TypeError: connect() got an unexpected keyword argument 'channel_binding'
# `sslmode` is popped separately because it carries meaning we must honour.
_LIBPQ_ONLY_PARAMS = (
    "channel_binding",
    "gssencmode",
    "sslrootcert",
    "sslcert",
    "sslkey",
    "sslnegotiation",
    "target_session_attrs",
)


def _ssl_context(mode: str) -> ssl.SSLContext | bool:
    """Translate a libpq sslmode into what asyncpg wants, keeping libpq's
    meaning: `require` encrypts without authenticating the server, and only
    `verify-ca`/`verify-full` actually validate the certificate."""
    if mode == "disable":
        return False
    ctx = ssl.create_default_context()
    if mode == "verify-full":
        return ctx  # verify chain + hostname (create_default_context default)
    if mode == "verify-ca":
        ctx.check_hostname = False
        return ctx
    # allow / prefer / require
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _prepare_connection() -> tuple[str, dict]:
    """Return (async URL, connect_args) with libpq-only parameters moved out of
    the query string and into arguments asyncpg accepts."""
    url = settings.database_url
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    parsed = urlsplit(url)
    params = dict(parse_qsl(parsed.query, keep_blank_values=True))
    sslmode = params.pop("sslmode", None)
    for name in _LIBPQ_ONLY_PARAMS:
        params.pop(name, None)
    url = urlunsplit(parsed._replace(query=urlencode(params)))

    connect_args: dict = {}
    managed = any(h in url for h in _MANAGED_HOSTS)
    if sslmode:
        connect_args["ssl"] = _ssl_context(sslmode)
    elif managed:
        # No sslmode given, but these providers mandate TLS anyway.
        connect_args["ssl"] = _ssl_context("require")
    if managed:
        connect_args["statement_cache_size"] = 0

    return url, connect_args


def get_async_database_url() -> str:
    """Async-dialect URL, stripped of parameters asyncpg cannot accept."""
    return _prepare_connection()[0]


def _build_connect_args() -> dict:
    return _prepare_connection()[1]


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
