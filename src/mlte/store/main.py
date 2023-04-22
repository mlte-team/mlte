"""
store/frontend/main.py

Application entry point.
"""

import logging
import sys

import uvicorn
from mlte.store.api.api import api_router
import mlte.store.backend as backend
import mlte.store.backend.engine as engine
import mlte.store.app_factory as app_factory
from mlte.store.core.config import settings

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def run(host: str, port: int, backend_uri: str):
    """
    Run the artifact store application.
    """
    # The global FastAPI application
    app = app_factory.create()

    # Initialize the backend
    engine.create_engine(backend_uri)

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
