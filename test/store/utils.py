"""Utils for MLTE store unit tests."""

from typing import Generator

from mlte._private import url as url_utils
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.user.model import RoleType
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI


def store_types() -> Generator[StoreType, None, None]:
    """
    Yield catalog store types.
    :return: Store type.
    """
    for store_type in StoreType:
        yield store_type


def create_api_and_http_uri(
    uri: StoreURI,
    catalog_uris: dict[str, StoreURI] = {},
) -> tuple[OAuthHttpClient, StoreURI]:
    """
    Get the params to configure an HTTP store, creating a test API.
    :return: The client to the test API, and the URI to connect.
    """
    # Create a user for the API. Use the one provided in the URI if any.
    _, username, password = url_utils.remove_url_username_password(uri.uri)
    if not username and not password:
        user = user_generator.build_admin_user()
        store_uri = StoreURI.from_string(
            url_utils.set_url_username_password(
                uri.uri, user.username, user.password
            )
        )
    else:
        assert username and password
        user = user_generator.build_test_user(
            username=username, password=password, role=RoleType.ADMIN
        )
        store_uri = uri

    test_api = TestAPI(user=user, catalog_uris=catalog_uris)
    client = test_api.get_test_client()

    return client, store_uri
