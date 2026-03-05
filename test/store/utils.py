"""Utils for MLTE store unit tests."""

from typing import Generator, Optional

from mlte._private import url as url_utils
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.user.model import UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.defaults import get_http_defaults_if_needed


def store_types() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in StoreType:
        yield store_fixture_name.value


def create_api_and_http_uri(
    user: Optional[UserWithPassword] = None, default_catalog_id: str = None
) -> tuple[OAuthHttpClient, str]:
    """
    Get the params to configure an HTTP store, creating a test API.
    :return: The client to the test API, and the URI to connect.
    """
    user = user_generator.build_admin_user()
    test_api = TestAPI(user=user, default_catalog_id=default_catalog_id)
    client = test_api.get_test_client()

    username, password, uri = get_http_defaults_if_needed(
        client.username, client.password, str(client.client.base_url)
    )
    uri = StoreURI.from_string(
        url_utils.set_url_username_password(uri, username, password)
    )

    return client, uri
