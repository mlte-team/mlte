"""
mlte/web/store/core/config.py

Configuration management for FastAPI application.
"""

from __future__ import annotations

from pydantic import BaseSettings, validator

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

    @validator("APP_PORT", pre=True)
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

    @validator("LOG_LEVEL", pre=True)
    def validate_log_level(cls, v: str) -> str:
        if v not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {v}.")
        return v

    class Config:
        case_sensitive = True


# The exported settings object
settings = Settings()
