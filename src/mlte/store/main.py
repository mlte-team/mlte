"""
store/frontend/main.py

Application entry point.
"""

import logging
import sys

import uvicorn
from fastapi import FastAPI
from mlte.store.api.api import api_router
import mlte.store.backend as backend
from mlte.store.core.config import settings

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The global FastAPI application
g_app = FastAPI(
    title="MLTE Artifact Store",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
)


def main() -> int:
    # TODO(Kyle): use log level.
    logging.basicConfig(level=logging.INFO)

    # Initialize the backend
    backend.initialize_engine()

    # Inject routes
    g_app.include_router(api_router, prefix=settings.API_PREFIX)

    # Run the server
    uvicorn.run(g_app, host=settings.APP_HOST, port=int(settings.APP_PORT))
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
