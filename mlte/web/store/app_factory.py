"""
mlte/web/store/app_factory.py

Web application factory.
"""

from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic.networks import HttpUrl

from mlte.web.store.core.config import settings


def create(*, allowed_origins: List[HttpUrl] = []) -> FastAPI:
    """
    Create an instance of the application.
    :param allowed_origins: A collection of allowed origins
    :return: The app
    """
    app = FastAPI(
        title="MLTE Artifact Store",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(url) for url in allowed_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
