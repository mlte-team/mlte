"""
mlte/web/store/app_factory.py

Web application factory.
"""

from fastapi import FastAPI

from mlte.backend.core.config import settings


def create() -> FastAPI:
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
    return app
