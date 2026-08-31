"""Connection-string handling for the orchestrator's Postgres.

Managed providers hand out libpq-flavoured URLs. SQLAlchemy forwards unknown
query parameters to asyncpg as keyword arguments, and asyncpg rejects the ones
libpq invented — so the URL has to be sanitised before the engine is built.

This matters more than it looks. A failure here surfaces as `database:
unavailable` on /health and nothing else, because get_db() yields None instead
of raising: exactly the symptom that was misdiagnosed for 2.5 months as a
Cloud SQL problem (BUG_LOG DL-024).
"""

import ssl

import pytest

from src.database.session import _prepare_connection

NEON = (
    "postgresql://u:p@ep-x-pooler.eu-central-1.aws.neon.tech/db"
    "?sslmode=require&channel_binding=require"
)


def _prep(monkeypatch, url):
    from src.database import session

    monkeypatch.setattr(session.settings, "database_url", url)
    return _prepare_connection()


def test_neon_url_drops_params_asyncpg_cannot_accept(monkeypatch):
    """The regression: `channel_binding` reached asyncpg.connect() and raised
    TypeError: connect() got an unexpected keyword argument 'channel_binding'."""
    url, args = _prep(monkeypatch, NEON)
    assert "channel_binding" not in url
    assert "sslmode" not in url
    assert url.startswith("postgresql+asyncpg://")
    assert isinstance(args["ssl"], ssl.SSLContext)


def test_neon_disables_the_prepared_statement_cache(monkeypatch):
    """Neon's pooled endpoint is PgBouncer in transaction mode, which cannot
    carry asyncpg's prepared statements."""
    _, args = _prep(monkeypatch, NEON)
    assert args["statement_cache_size"] == 0


def test_plain_local_url_is_left_alone(monkeypatch):
    url, args = _prep(monkeypatch, "postgresql://postgres:postgres@localhost:5432/compliance")
    assert url == "postgresql+asyncpg://postgres:postgres@localhost:5432/compliance"
    assert args == {}


@pytest.mark.parametrize(
    "mode,expected_verify,expected_hostname",
    [
        ("require", ssl.CERT_NONE, False),
        ("verify-ca", ssl.CERT_REQUIRED, False),
        ("verify-full", ssl.CERT_REQUIRED, True),
    ],
)
def test_sslmode_is_translated_not_discarded(
    monkeypatch, mode, expected_verify, expected_hostname
):
    """Dropping sslmode wholesale would silently downgrade TLS on any provider
    outside the managed list — a security regression that no test would catch."""
    _, args = _prep(monkeypatch, f"postgresql://u:p@db.example.com/x?sslmode={mode}")
    ctx = args["ssl"]
    assert ctx.verify_mode == expected_verify
    assert ctx.check_hostname is expected_hostname


def test_sslmode_disable_means_no_tls(monkeypatch):
    _, args = _prep(monkeypatch, "postgresql://u:p@db.example.com/x?sslmode=disable")
    assert args["ssl"] is False
