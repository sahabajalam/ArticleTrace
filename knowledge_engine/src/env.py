"""Repo-root `.env` discovery and loud credential checks.

The repo keeps exactly one `.env`, at the repo root. Resolving it relative to
the process working directory means a script launched from `knowledge_engine/`
looks for `knowledge_engine/.env`, finds nothing, and silently falls back to
field defaults — that is BUG_LOG DL-025 step 2, where the service kept talking
to a dead Neo4j instance after the root `.env` had been updated.

Everything here derives from `__file__`, so the answer is the same no matter
where the process was launched from.

The orchestrator ships the same helper (`orchestrator/src/env.py`). The two
services build into separate images and share no package, so the duplication is
deliberate — do not replace it with a cross-service import.
"""

from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path | None = None) -> Path:
    """Return the repo root for `start` (defaults to this file).

    Prefers the `.git` marker: it identifies the root even when the root `.env`
    is absent (fresh clone — `.env` is gitignored), and it makes a stray
    per-service `.env` lose to the root one rather than shadow it. Falls back to
    the nearest ancestor holding a `.env` for installed copies that have no
    `.git`, and finally to the service's parent directory.
    """
    here = (start or Path(__file__)).resolve()
    for parent in here.parents:
        if (parent / ".git").exists():
            return parent
    for parent in here.parents:
        if (parent / ".env").is_file():
            return parent
    # Neither marker (e.g. a container that copies only `src/`): assume the
    # layout this file lives in — <root>/<service>/src/env.py.
    return here.parents[min(2, len(here.parents) - 1)]


def find_env_file(start: Path | None = None) -> Path:
    """Absolute path of the repo-root `.env`, whether or not it exists.

    A missing file is fine: pydantic-settings ignores it and reads real
    environment variables instead, which is how Cloud Run is configured.
    """
    return find_repo_root(start) / ".env"


ENV_FILE = find_env_file()


class MissingCredentialError(RuntimeError):
    """A credential required at startup is absent or empty."""

    def __init__(self, variable: str, env_file: Path | None = None) -> None:
        where = f", or add it to {env_file}" if env_file is not None else ""
        super().__init__(
            f"{variable} is not set. Export it as an environment variable{where}."
        )
        self.variable = variable
        self.env_file = env_file


def require_credential(
    value: str | None, variable: str, env_file: Path | None = ENV_FILE
) -> str:
    """Return `value`, or raise naming the variable and where it was expected."""
    if not (value or "").strip():
        raise MissingCredentialError(variable, env_file)
    return value
