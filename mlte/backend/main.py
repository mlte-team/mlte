"""Entry point for MLTE artifact store server."""

import logging
import sys
from typing import Any

import uvicorn
from pydantic.networks import HttpUrl

import mlte._private.hosts as util
import mlte.backend.core.app_factory as app_factory
from mlte.backend.core.config import settings
from mlte.backend.core.state import state
from mlte.session.session_stores import setup_stores
from mlte.store.base import StoreType, StoreURI

# Application exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Wildcard for any URL.
ANY_URL = "*"


def _validate_origins(allowed_origins: list[str]) -> list[Any]:
    """
    Validate allowed origins.
    :param allowed_origins: The collection of allowed origins, as strings
    :raises ValidationError: If validation fails
    :return: The parsed allowed origins
    """
    return [HttpUrl(url) if url != ANY_URL else url for url in allowed_origins]


def run(
    host: str,
    port: int,
    store_uri: str,
    catalog_uris: dict[str, str],
    allowed_origins: list[str],
    jwt_secret: str,
) -> int:
    """
    Run the artifact store application.
    :param host: The application host
    :param port: The application port
    :param store_uri: The store URI string
    :param catalog_uris: A dict of URIs for catalog stores
    :param allowed_origins: A list of allowed CORS origins
    :param jwt_secret: A secret random string key used to sign tokens
    :return: Return code
    """
    # TODO(Kyle): use log level from arguments.
    logging.basicConfig(level=logging.INFO)

    # Resolve hosts and validate resolved origins.
    allowed_origins = util.resolve_hosts(allowed_origins)
    _ = _validate_origins(allowed_origins)
    logging.info(f"Allowed origins: {allowed_origins}")

    # The global FastAPI application
    app = app_factory.create(allowed_origins)

    # Setup all stores.
    _setup_stores(store_uri, catalog_uris)

    # Set the token signing key.
    state.set_token_key(jwt_secret)

    # Run the server
    uvicorn.run(app, host=host, port=port)
    return EXIT_SUCCESS


def _setup_stores(stores_uri: str, catalog_uris: dict[str, str]):
    """
    Sets up all stores required by MLTE, from the provided URIs.

    :param stores_uri: The store URI string, used as the common type and root location for all non-catalog stores.
    :param catalog_uris: A dict of URIs for catalog stores.
    """
    parsed_uri = StoreURI.from_string(stores_uri)
    logging.info(f"Backend using stores URI of type: {parsed_uri.type}")
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        raise RuntimeError("Cannot run backend with HTTP artifact store.")

    logging.info(f"Backend will add catalog stores: {catalog_uris}")

    state.stores = setup_stores(stores_uri, catalog_uris)


def main() -> int:
    return run(
        settings.BACKEND_HOST,
        int(settings.BACKEND_PORT),
        settings.STORE_URI,
        settings.CATALOG_URIS,
        settings.ALLOWED_ORIGINS,
        settings.JWT_SECRET_KEY,
    )


if __name__ == "__main__":
    sys.exit(main())
