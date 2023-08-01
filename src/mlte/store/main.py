"""
mlte/store/frontend/main.py

Application entry point.
"""

import logging
import sys

import uvicorn
from mlte.store.api.api import api_router
from mlte.store.backend.engine import create_engine
from mlte.store.state import state
import mlte.store.app_factory as app_factory
from mlte.store.core.config import settings

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def run(host: str, port: int, backend_uri: str) -> int:
    """
    Run the artifact store application.
    :param host: The application host
    :type host: str
    :param port: The application port
    :type port: int
    :param backend_uri: The backend URI string
    :type backend_uri: str
    :return: Return code
    :rtype: int
    """
    # The global FastAPI application
    app = app_factory.create()

    # Initialize the backend engine
    engine = create_engine(backend_uri)
    state.set_engine(engine)

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
