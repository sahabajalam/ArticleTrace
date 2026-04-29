"""Standalone configuration for EU AI Knowledge Base."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Neo4j (also hosts the native vector index — see graph_store.vector_search)
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


settings = Settings()
