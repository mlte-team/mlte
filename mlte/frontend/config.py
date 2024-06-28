"""
mlte/frontend/config.py

Configuration management for the frontend.
"""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# An enumeration of supported log levels
_LOG_LEVELS = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """
    The BaseSettings class from pydantic automatically manages
    reading environment variables from the environment or a
    .env file if configured properly.
    """

    ENVIRONMENT: str = "default"
    """Used to check the type of settings being used."""

    FRONTEND_HOST: str = "localhost"
    """The host to which the frontend server binds."""

    FRONTEND_PORT: str = "8000"
    """The port to which the frontend server binds."""

    @field_validator("FRONTEND_PORT", mode="before")
    @classmethod
    def validate_app_port(cls, v: str) -> str:
        try:
            int(v)
        except ValueError:
            raise ValueError(
                f"Failed to parse int from FRONTEND_PORT: {v}."
            ) from None
        return v

    LOG_LEVEL: str = "ERROR"
    """The application log level; defaults to ERROR."""

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if v not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {v}.")
        return v

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env.frontend"
    )


# The exported settings object
settings = Settings()
