"""
mlte/backend/main.py

Entry point for MLTE artifact store server.
"""

import logging
import sys
from typing import Any

import uvicorn
from pydantic.networks import HttpUrl

import mlte._private.hosts as util
import mlte.backend.core.app_factory as app_factory
from mlte.backend.core.config import settings
from mlte.backend.core.state import state
from mlte.store.artifact import factory as artifact_store_factory
from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.sample_catalog import SampleCatalog
from mlte.store.custom_list.initial_custom_lists import InitialCustomLists
from mlte.store.user import factory as user_store_factory

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

    # Initialize the backing artifact store instance.
    artifact_store = artifact_store_factory.create_artifact_store(stores_uri)
    if artifact_store.uri.type == StoreType.REMOTE_HTTP:
        raise RuntimeError("Cannot run backend with HTTP artifact store.")
    state.set_artifact_store(artifact_store)

    # Initialize the backing user store instance. Assume same store as artifact one for now.
    # TODO: allow for separate config of uri here?
    user_store = user_store_factory.create_user_store(stores_uri)
    state.set_user_store(user_store)

    # Initialize the backing custom list store instance. Assume same store as artifact one for now.
    # TODO: allow for separate config of uri here?
    custom_list_store = InitialCustomLists.setup_custom_list_store(stores_uri)
    state.set_custom_list_store(custom_list_store)

    # Catalogs: first add the sample catalog store.
    sample_catalog = SampleCatalog.setup_sample_catalog(stores_uri)
    state.add_catalog_store(
        store=sample_catalog, id=SampleCatalog.SAMPLE_CATALOG_ID
    )

    # Catalogs: Add all configured catalog stores.
    for id, uri in catalog_uris.items():
        logging.info(
            f"Adding catalog with id '{id}' and URI of type: {StoreURI.from_string(uri).type}"
        )
        state.add_catalog_store_from_uri(uri, id)


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
