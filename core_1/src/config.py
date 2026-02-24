"""Configuration management using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/monitoring"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8002
    log_level: str = "INFO"

    # Slack Alerting
    slack_webhook_url: str | None = None
    slack_channel: str = "#ai-compliance-alerts"

    # Email Alerting
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    alert_email_to: str | None = None

    # Compliance Thresholds
    human_review_target_rate: float = 0.10
    max_human_override_rate: float = 0.15
    drift_threshold: float = 0.10
    bias_p_value_threshold: float = 0.05

    # Prometheus
    prometheus_port: int = 9090

    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 10


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
