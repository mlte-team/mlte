"""
mlte/backend/app_factory.py

Web application factory.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mlte.backend.api.api import api_router
from mlte.backend.api.auth.http_auth_exception import (
    HTTPTokenException,
    json_content_exception_handler,
)
from mlte.backend.core.config import settings


def create(allowed_origins: list[str] = []) -> FastAPI:
    """
    Create an instance of the application.
    :return: The app
    """
    app = FastAPI(
        title="MLTE Artifact Store",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )

    # Inject routes
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Attach middleware
    # NOTE(Kyle): It is imporant middleware is applied AFTER routes are injected
    if len(allowed_origins) > 0:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add proper exception handling for Token responses, to be OAuth compliant.
    app.add_exception_handler(
        HTTPTokenException, json_content_exception_handler  # type: ignore
    )

    return app
