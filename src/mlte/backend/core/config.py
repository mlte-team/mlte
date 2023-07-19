"""
store/core/config.py

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

    # The global API prefix string
    API_PREFIX: str = "/api"

    # The host and port to which the server binds
    APP_HOST: str = "localhost"
    APP_PORT: str = "8080"

    @validator("APP_PORT", pre=True)
    def validate_app_port(cls, v: str) -> str:
        try:
            int(v)
        except ValueError:
            raise ValueError(
                f"Failed to parse int from APP_PORT: {v}."
            ) from None
        return v

    # The backend URI string
    BACKEND_URI: str = "fs://./store"

    # The application logging level
    LOG_LEVEL: str = "ERROR"

    @validator("LOG_LEVEL", pre=True)
    def validate_log_level(cls, v: str) -> str:
        if v not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {v}.")
        return v

    class Config:
        case_sensitive = True


# The exported settings object
settings = Settings()
