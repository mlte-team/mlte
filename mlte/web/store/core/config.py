"""
mlte/web/store/core/config.py

Configuration management for FastAPI application.
"""

from __future__ import annotations

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# An enumeration of supported log levels
_LOG_LEVELS = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """
    The BaseSettings class from pydantic automatically manages
    reading environment variables from the environment or a
    .env file is configured properly.
    """

    API_PREFIX: str = "/api"
    """The global API prefix."""

    APP_HOST: str = "localhost"
    """The host to which the server binds."""

    APP_PORT: str = "8080"
    """The port to which the server binds."""

    @field_validator("APP_PORT", mode="before")
    @classmethod
    def validate_app_port(cls, v: str) -> str:
        try:
            int(v)
        except ValueError:
            raise ValueError(
                f"Failed to parse int from APP_PORT: {v}."
            ) from None
        return v

    BACKEND_URI: str = "memory://"
    """The backend URI string; defaults to in-memory backend."""

    LOG_LEVEL: str = "ERROR"
    """The application log level; defaults to ERROR."""

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if v not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {v}.")
        return v

    ALLOWED_ORIGINS: List[str] = []
    """A list of allowed CORS origins."""

    model_config = SettingsConfigDict(case_sensitive=True)


# The exported settings object
settings = Settings()
