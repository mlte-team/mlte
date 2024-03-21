"""
mlte/web/store/main.py

Entry point for MLTE artifact store server.
"""

import logging
import sys
from typing import List

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic.networks import HttpUrl

import mlte.backend.app_factory as app_factory
import mlte.backend.util.origins as util
from mlte.backend.api.api import api_router
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.store.artifact.factory import create_store
from mlte.store.base import StoreType

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def _validate_origins(allowed_origins: List[str]) -> List[HttpUrl]:
    """
    Validate allowed origins.
    :param allowed_origins: The collection of allowed origins, as strings
    :raises ValidationError: If validation fails
    :return: The parsed allowed origins
    """
    return [HttpUrl(url) for url in allowed_origins]


def run(
    host: str, port: int, backend_uri: str, allowed_origins: List[str]
) -> int:
    """
    Run the artifact store application.
    :param host: The application host
    :param port: The application port
    :param backend_uri: The backend URI string
    :param allowed_origins: A list of allowed CORS origins
    :return: Return code
    """
    # Resolve hosts
    allowed_origins = util.resolve_hosts(allowed_origins)
    # Validate resolved origins
    _ = _validate_origins(allowed_origins)

    # The global FastAPI application
    app = app_factory.create()

    # Inject routes
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Attach middleware
    # NOTE(Kyle): It is imporant middleware is applied AFTER routes are injected
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize the backing store instance
    store = create_store(backend_uri)
    if store.uri.type == StoreType.REMOTE_HTTP:
        raise RuntimeError(
            "Cannot run artifact store server with remote HTTP backend."
        )
    state.set_store(store)

    # Run the server
    uvicorn.run(app, host=host, port=port)
    return EXIT_SUCCESS


def main() -> int:
    # TODO(Kyle): use log level.
    logging.basicConfig(level=logging.INFO)
    return run(
        settings.APP_HOST,
        int(settings.APP_PORT),
        settings.BACKEND_URI,
        settings.ALLOWED_ORIGINS,
    )


if __name__ == "__main__":
    sys.exit(main())
