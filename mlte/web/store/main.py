"""
mlte/web/store/main.py

Entry point for MLTE artifact store server.
"""

import logging
import sys

import uvicorn

import mlte.web.store.app_factory as app_factory
from mlte.store.base import StoreType
from mlte.store.factory import create_store
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def run(host: str, port: int, backend_uri: str) -> int:
    """
    Run the artifact store application.
    :param host: The application host
    :param port: The application port
    :param backend_uri: The backend URI string
    :return: Return code
    """
    # The global FastAPI application
    app = app_factory.create()

    # Initialize the backing store instance
    store = create_store(backend_uri)
    if store.uri.type == StoreType.REMOTE_HTTP:
        raise RuntimeError(
            "Cannot run artifact store server with remote HTTP backend."
        )
    state.set_store(store)

    # Inject routes
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Run the server
    uvicorn.run(app, host=host, port=port)
    return EXIT_SUCCESS


def main() -> int:
    # TODO(Kyle): use log level.
    logging.basicConfig(level=logging.INFO)
    return run(settings.APP_HOST, int(settings.APP_PORT), settings.BACKEND_URI)


if __name__ == "__main__":
    sys.exit(main())
