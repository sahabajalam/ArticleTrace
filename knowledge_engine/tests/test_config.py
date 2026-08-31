"""Tests for CWD-independent `.env` resolution and loud credential failures."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))

# `src.config` validates credentials when it is imported — that is the point of
# this module — so give it something to find first. `setdefault` keeps a real
# key from the environment if one is already exported.
os.environ.setdefault("GOOGLE_API_KEY", "test-google-api-key")

from src.config import Settings  # noqa: E402
from src.env import (  # noqa: E402
    ENV_FILE,
    MissingCredentialError,
    find_env_file,
    find_repo_root,
    require_credential,
)
from src.stores.graph_store import GraphStore  # noqa: E402


# ── Env file resolution ───────────────────────────────────────────────────────

class TestEnvFileResolution:
    def test_env_file_is_the_repo_root_one(self):
        assert ENV_FILE == REPO_ROOT / ".env"
        assert ENV_FILE.is_absolute()

    @pytest.mark.parametrize("cwd", ["repo_root", "service_dir", "tmp"])
    def test_resolution_is_independent_of_cwd(self, cwd, tmp_path, monkeypatch):
        """The bug: running from knowledge_engine/ looked for knowledge_engine/.env."""
        monkeypatch.chdir(
            {"repo_root": REPO_ROOT, "service_dir": PROJECT_ROOT, "tmp": tmp_path}[cwd]
        )
        assert find_env_file() == REPO_ROOT / ".env"

    def test_settings_uses_the_absolute_path(self):
        assert Settings.model_config["env_file"] == REPO_ROOT / ".env"

    def test_git_marker_identifies_the_root(self, tmp_path):
        root = tmp_path / "repo"
        (root / ".git").mkdir(parents=True)
        module = root / "service" / "src" / "config.py"
        module.parent.mkdir(parents=True)
        module.touch()

        assert find_repo_root(module) == root
        assert find_env_file(module) == root / ".env"

    def test_a_stray_service_env_does_not_shadow_the_root(self, tmp_path):
        """DL-025: a stale knowledge_engine/.env must not win over the root one."""
        root = tmp_path / "repo"
        (root / ".git").mkdir(parents=True)
        (root / ".env").write_text("NEO4J_URI=bolt://root:7687\n")
        module = root / "service" / "src" / "config.py"
        module.parent.mkdir(parents=True)
        module.touch()
        (root / "service" / ".env").write_text("NEO4J_URI=bolt://stale:7687\n")

        assert find_env_file(module) == root / ".env"

    def test_falls_back_to_nearest_env_without_a_git_dir(self, tmp_path):
        """Installed copies (no .git) still find a `.env` above them."""
        root = tmp_path / "deployed"
        module = root / "service" / "src" / "config.py"
        module.parent.mkdir(parents=True)
        module.touch()
        (root / ".env").write_text("NEO4J_URI=bolt://deployed:7687\n")

        assert find_env_file(module) == root / ".env"


# ── Precedence ────────────────────────────────────────────────────────────────

class TestPrecedence:
    def test_environment_variable_beats_the_env_file(self, tmp_path, monkeypatch):
        """Cloud Run injects real env vars; they must outrank the file."""
        env_file = tmp_path / ".env"
        env_file.write_text(
            "NEO4J_URI=bolt://from-file:7687\nGOOGLE_API_KEY=key-from-file\n"
        )
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.setenv("NEO4J_URI", "bolt://from-environment:7687")

        settings = Settings(_env_file=env_file)

        assert settings.neo4j_uri == "bolt://from-environment:7687"
        # Unset in the environment, so this one still comes from the file.
        assert settings.google_api_key == "key-from-file"


# ── Missing credentials ───────────────────────────────────────────────────────

class TestMissingCredentials:
    def test_absent_google_api_key_names_the_variable(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)

        with pytest.raises(MissingCredentialError) as exc_info:
            Settings(_env_file=None)

        message = str(exc_info.value)
        assert "GOOGLE_API_KEY" in message
        assert str(ENV_FILE) in message

    def test_empty_google_api_key_also_raises(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "   ")

        with pytest.raises(MissingCredentialError) as exc_info:
            Settings(_env_file=None)

        assert exc_info.value.variable == "GOOGLE_API_KEY"

    def test_present_google_api_key_constructs(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_API_KEY", "a-real-looking-key")

        assert Settings(_env_file=None).google_api_key == "a-real-looking-key"

    def test_graph_store_rejects_an_empty_password(self):
        """Checked at client construction, so importing the module stays cheap."""
        with pytest.raises(MissingCredentialError) as exc_info:
            GraphStore(uri="bolt://localhost:7687", user="neo4j", password="")

        assert "NEO4J_PASSWORD" in str(exc_info.value)

    def test_require_credential_returns_the_value(self):
        assert require_credential("value", "SOME_VAR") == "value"
