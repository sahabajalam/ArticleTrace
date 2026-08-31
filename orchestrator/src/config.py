"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator

from .env import ENV_FILE, require_credential


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # `env_file` is the absolute repo-root path, not a CWD-relative ".env", so
    # the service picks up the same file whether it is launched from the repo
    # root or from orchestrator/. Real environment variables still take
    # priority over the file — Cloud Run relies on that.
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM API Keys
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    anthropic_api_key: str = Field(default="", description="Anthropic API key for Claude")

    # Database
    database_url: str = Field(
        default="postgresql://localhost:5432/compliance_agent",
        description="PostgreSQL connection URL",
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", description="Redis connection URL")

    # Project Integration URLs
    graphrag_api_url: str = Field(
        default="http://localhost:8001",
        description="Knowledge Engine GraphRAG API URL for legal research",
    )

    # Alerting
    slack_webhook_url: str = Field(default="", description="Slack webhook for alerts")

    # Cost Management
    max_daily_spend_usd: float = Field(
        default=50.0, description="Maximum daily spend on LLM APIs"
    )
    max_spend_per_assessment_usd: float = Field(
        default=5.0, description="Maximum spend per compliance assessment"
    )

    # Environment
    environment: str = Field(default="development", description="Runtime environment")
    log_level: str = Field(default="INFO", description="Logging level")

    # LLM Model Configuration
    primary_model: str = Field(default="gemini-2.5-flash", description="Primary LLM for complex reasoning")
    secondary_model: str = Field(
        default="gemini-2.5-flash", description="Secondary LLM for simple tasks"
    )
    fallback_model: str = Field(
        default="gemini-2.5-flash", description="Fallback LLM"
    )
    ast_reviewer_model: str = Field(
        default="gemini-2.5-flash-lite",
        description="Fast, cheap LLM used to semantically review AST decision surfaces",
    )
    ast_reviewer_max_surfaces: int = Field(
        default=50,
        description="Cap on decision surfaces sent to the LLM reviewer per scan",
    )
    ast_reviewer_batch_size: int = Field(
        default=8,
        description="Decision surfaces per LLM batch call",
    )

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8080",
        description="Comma-separated list of allowed CORS origins",
    )
    cors_allow_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS requests",
    )

    @model_validator(mode="after")
    def _require_gemini_api_key(self) -> "Settings":
        """`Field(...)` catches an absent key; this also catches an empty one."""
        require_credential(self.gemini_api_key, "GEMINI_API_KEY", ENV_FILE)
        return self

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string.

        Supports wildcard '*' as a value in the list to allow all origins
        (useful for Cloud Run deployments where the frontend URL is dynamic).
        """
        origins = [o.strip() for o in self.cors_origins.split(",") if o.strip()]
        if "*" in origins:
            return ["*"]
        return origins


settings = Settings()
