"""
mlte/backend/main.py

Entry point for MLTE artifact store server.
"""

import logging
import sys
from typing import List

import uvicorn
from pydantic.networks import HttpUrl

import mlte.backend.app_factory as app_factory
import mlte.backend.util.origins as util
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.store.artifact import factory as artifact_store_factory
from mlte.store.base import StoreType
from mlte.store.user import factory as user_store_factory

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
    host: str,
    port: int,
    store_uri: str,
    allowed_origins: List[str],
    jwt_secret: str,
) -> int:
    """
    Run the artifact store application.
    :param host: The application host
    :param port: The application port
    :param store_uri: The store URI string
    :param allowed_origins: A list of allowed CORS origins
    :param jwt_secret: A secret random string key used to sign tokens
    :return: Return code
    """
    # Resolve hosts and validate resolved origins.
    allowed_origins = util.resolve_hosts(allowed_origins)
    _ = _validate_origins(allowed_origins)

    # The global FastAPI application
    app = app_factory.create(allowed_origins)

    # Initialize the backing artifact store instance
    store = artifact_store_factory.create_store(store_uri)
    if store.uri.type == StoreType.REMOTE_HTTP:
        raise RuntimeError("Cannot run backend with remote HTTP store.")
    state.set_artifact_store(store)

    # Initialize the backing user store instance. Assume same store as artifact one for now.
    # TODO: allow for separate config of uri here
    user_store = user_store_factory.create_store(store_uri)
    state.set_user_store(user_store)

    # Set the token signing key.
    state.set_token_key(jwt_secret)

    # Run the server
    uvicorn.run(app, host=host, port=port)
    return EXIT_SUCCESS


def main() -> int:
    # TODO(Kyle): use log level.
    logging.basicConfig(level=logging.INFO)
    return run(
        settings.APP_HOST,
        int(settings.APP_PORT),
        settings.STORE_URI,
        settings.ALLOWED_ORIGINS,
        settings.JWT_SECRET_KEY,
    )


if __name__ == "__main__":
    sys.exit(main())
