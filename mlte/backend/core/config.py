"""
mlte/backend/core/config.py

Configuration management for FastAPI application.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from mlte.store.base import StoreType, StoreURI

# An enumeration of supported log levels
_LOG_LEVELS = ["DEBUG", "WARNING", "INFO", "ERROR", "CRITICAL"]

# Default address for Frontend.
DEFAULT_FRONTEND_ADDRESS = "http://localhost:8000"


class Settings(BaseSettings):
    """
    The BaseSettings class from pydantic automatically manages
    reading environment variables from the environment or a
    .env file if configured properly.
    """

    ENVIRONMENT: str = "default"
    """Used to check the type of settings being used."""

    API_PREFIX: str = "/api"
    """The global API prefix."""

    BACKEND_HOST: str = "localhost"
    """The host to which the server binds."""

    BACKEND_PORT: str = "8080"
    """The port to which the server binds."""

    @field_validator("BACKEND_PORT", mode="before")
    @classmethod
    def validate_app_port(cls, v: str) -> str:
        try:
            int(v)
        except ValueError:
            raise ValueError(
                f"Failed to parse int from BACKEND_PORT: {v}."
            ) from None
        return v

    STORE_URI: str = StoreURI.get_default_prefix(StoreType.LOCAL_MEMORY)
    """The store URI string; defaults to in-memory store."""

    CATALOG_URIS: Dict[str, str] = {
        "local": StoreURI.get_default_prefix(StoreType.LOCAL_MEMORY)
    }
    """The dict of catalog URI strings; defaults to one in-memory store."""

    LOG_LEVEL: str = "ERROR"
    """The application log level; defaults to ERROR."""

    @field_validator("LOG_LEVEL", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if v not in _LOG_LEVELS:
            raise ValueError(f"Unsupported log level: {v}.")
        return v

    ALLOWED_ORIGINS: List[str] = [DEFAULT_FRONTEND_ADDRESS]
    """A list of allowed CORS origins."""

    JWT_SECRET_KEY: str = (
        "399fd92f61c99e35d7f2f6fdb9d65293c4047f9ac500af1886b8868b495f20b3"
    )
    """The secret key used to encode/decode JWT tokens."""

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env.backend"
    )


# The exported settings object
settings = Settings()
