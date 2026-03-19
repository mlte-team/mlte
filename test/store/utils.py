"""Utils for MLTE store unit tests."""

from typing import Generator, Optional

from mlte._private import url as url_utils
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.user.model import UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.defaults import get_http_defaults_if_needed


def store_types() -> Generator[StoreType, None, None]:
    """
    Yield catalog store types.
    :return: Store type.
    """
    for store_type in StoreType:
        yield store_type


def create_api_and_http_uri(
    user: Optional[UserWithPassword] = None,
    catalog_uris: dict[str, StoreURI] = {},
) -> tuple[OAuthHttpClient, StoreURI]:
    """
    Get the params to configure an HTTP store, creating a test API.
    :return: The client to the test API, and the URI to connect.
    """
    user = user_generator.build_admin_user()
    test_api = TestAPI(user=user, catalog_uris=catalog_uris)
    client = test_api.get_test_client()

    username, password, uri = get_http_defaults_if_needed(
        client.username, client.password, str(client.client.base_url)
    )
    store_uri = StoreURI.from_string(
        url_utils.set_url_username_password(uri, username, password)
    )

    return client, store_uri
