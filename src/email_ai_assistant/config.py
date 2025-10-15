"""Configuration loading for the Email AI Assistant."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field, validator


def _default_credentials_path() -> Path:
    return Path.home() / ".credentials" / "email-ai-assistant" / "credentials.json"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    google_application_credentials: Path = Field(
        default_factory=_default_credentials_path,
        alias="GOOGLE_APPLICATION_CREDENTIALS",
        description="Path to the Google OAuth credentials JSON file.",
    )
    primary_email: str = Field(
        alias="PRIMARY_EMAIL",
        description="Email address that should be analyzed by the assistant.",
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        alias="OPENAI_API_KEY",
        description="Optional API key used for LLM-powered enrichment steps.",
    )

    @validator("primary_email")
    def _validate_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("PRIMARY_EMAIL must be a valid email address")
        return value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
