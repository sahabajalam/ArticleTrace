"""Standalone configuration for EU AI Knowledge Base."""

from pathlib import Path

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .env import ENV_FILE, require_credential


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # `env_file` is the absolute repo-root path, not a CWD-relative ".env", so
    # scripts pick up the same file whether they are launched from the repo
    # root or from knowledge_engine/. Real environment variables still take
    # priority over the file — Cloud Run relies on that.
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Neo4j (also hosts the native vector index — see graph_store.vector_search)
    # neo4j_password is checked in GraphStore.__init__ instead of here, so that
    # tests which never connect can still import this module.
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Google AI
    google_api_key: str = ""
    embedding_model: str = "gemini-embedding-001"
    llm_model: str = "gemini-1.5-pro"

    # Data paths
    raw_data_dir: Path = Path("../Data")
    parsed_data_dir: Path = Path("./parsed_data")

    # Retrieval
    rrf_k: int = 60
    default_top_k: int = 10
    max_hops: int = 3

    @model_validator(mode="after")
    def _require_google_api_key(self) -> "Settings":
        """Fail at startup rather than as a 401 from Google several frames away."""
        require_credential(self.google_api_key, "GOOGLE_API_KEY", ENV_FILE)
        return self


settings = Settings()
