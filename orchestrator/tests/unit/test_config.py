"""Tests for CWD-independent `.env` resolution and loud credential failures."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parent

# `src.config` builds a Settings() when it is imported, and gemini_api_key is
# required — give it something to find first. `setdefault` keeps a real key from
# the environment if one is already exported.
os.environ.setdefault("GEMINI_API_KEY", "test-gemini-api-key")

from src.config import Settings  # noqa: E402
from src.env import (  # noqa: E402
    ENV_FILE,
    MissingCredentialError,
    find_env_file,
    find_repo_root,
)


# ── Env file resolution ───────────────────────────────────────────────────────

class TestEnvFileResolution:
    def test_env_file_is_the_repo_root_one(self):
        assert ENV_FILE == REPO_ROOT / ".env"
        assert ENV_FILE.is_absolute()

    @pytest.mark.parametrize("cwd", ["repo_root", "service_dir", "tmp"])
    def test_resolution_is_independent_of_cwd(self, cwd, tmp_path, monkeypatch):
        """The bug: running from orchestrator/ looked for orchestrator/.env."""
        monkeypatch.chdir(
            {"repo_root": REPO_ROOT, "service_dir": PROJECT_ROOT, "tmp": tmp_path}[cwd]
        )
        assert find_env_file() == REPO_ROOT / ".env"

    def test_settings_uses_the_absolute_path(self):
        assert Settings.model_config["env_file"] == REPO_ROOT / ".env"

    def test_a_stray_service_env_does_not_shadow_the_root(self, tmp_path):
        """DL-025: a stale per-service .env must not win over the root one."""
        root = tmp_path / "repo"
        (root / ".git").mkdir(parents=True)
        (root / ".env").write_text("GEMINI_API_KEY=root\n")
        module = root / "service" / "src" / "config.py"
        module.parent.mkdir(parents=True)
        module.touch()
        (root / "service" / ".env").write_text("GEMINI_API_KEY=stale\n")

        assert find_repo_root(module) == root
        assert find_env_file(module) == root / ".env"


# ── Precedence ────────────────────────────────────────────────────────────────

class TestPrecedence:
    def test_environment_variable_beats_the_env_file(self, tmp_path, monkeypatch):
        """Cloud Run injects real env vars; they must outrank the file."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "GEMINI_API_KEY=key-from-file\nLOG_LEVEL=DEBUG\nENVIRONMENT=from-file\n"
        )
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        settings = Settings(_env_file=env_file)

        assert settings.log_level == "WARNING"
        # Unset in the environment, so this one still comes from the file.
        assert settings.environment == "from-file"


# ── Missing credentials ───────────────────────────────────────────────────────

class TestMissingCredentials:
    def test_absent_gemini_api_key_names_the_variable(self, monkeypatch):
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        with pytest.raises(ValidationError) as exc_info:
            Settings(_env_file=None)

        assert "gemini_api_key" in str(exc_info.value)

    def test_empty_gemini_api_key_names_the_variable(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "   ")

        with pytest.raises(MissingCredentialError) as exc_info:
            Settings(_env_file=None)

        message = str(exc_info.value)
        assert "GEMINI_API_KEY" in message
        assert str(ENV_FILE) in message

    def test_present_gemini_api_key_constructs(self, monkeypatch):
        monkeypatch.setenv("GEMINI_API_KEY", "a-real-looking-key")

        assert Settings(_env_file=None).gemini_api_key == "a-real-looking-key"
