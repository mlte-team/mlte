"""
test/backend/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

import typing
from typing import Any, Callable, Dict, Optional

import httpx
import pytest
from fastapi.testclient import TestClient

import test.backend.fixture.api_helper as api_helpers
from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.model.base_model import BaseModel
from mlte.store.common.http_clients import HttpClientType, OAuthHttpClient
from mlte.user.model import UserWithPassword

# -----------------------------------------------------------------------------
# Test HTTP client based on FastAPI's TestClient.
# -----------------------------------------------------------------------------


class FastAPITestHttpClient(OAuthHttpClient):
    """An HTTP client based on FastAPI's TestClient."""

    def __init__(
        self,
        client: TestClient,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        super().__init__(HttpClientType.TESTCLIENT, username, password)

        self.client = client
        """The underlying client."""

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self.client.get(url, headers=self.headers, **kwargs)

    def post(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.post(
            url, headers=self.headers, data=data, json=json, **kwargs
        )

    def put(
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.put(
            url, headers=self.headers, data=data, json=json, **kwargs
        )

    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self.client.delete(url, headers=self.headers, **kwargs)


# -----------------------------------------------------------------------------
# Store Backend Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture(scope="function")
def mem_store_and_test_http_client() -> (
    Callable[[Optional[UserWithPassword]], FastAPITestHttpClient]
):
    """Sets up memory based store for the API and gets an associated client."""

    def wrapper(api_user: Optional[UserWithPassword] = None) -> FastAPITestHttpClient:
        return setup_API_and_test_client(api_user)

    return wrapper


def setup_API_and_test_client(
    user: Optional[UserWithPassword] = None,
) -> FastAPITestHttpClient:
    """
    Configure API for memory stores and return a test HTTP client.
    :return: The client
    """
    if user is None:
        user = api_helpers.build_test_user()

    # Setup API, configure to use memory artifact store and create app itself.
    app = api_helpers.setup_api_with_mem_stores(user)

    # Create the test client, and authenticate to get token and allow protected endpoints to work.
    client = FastAPITestHttpClient(TestClient(app))
    client.username = user.username
    client.password = user.password
    client.authenticate(f"{settings.API_PREFIX}")
    return client


def get_client_for_admin(
    test_client: FastAPITestHttpClient,
) -> FastAPITestHttpClient:
    """Gets a client for the same app as the given one, but with an admin user."""
    admin_user = api_helpers.build_admin_user()
    admin_client = FastAPITestHttpClient(TestClient(test_client.client.app))
    admin_client.username = admin_user.username
    admin_client.password = admin_user.password
    admin_client.authenticate(f"{settings.API_PREFIX}")
    return admin_client


def admin_create_entity(
    entity: BaseModel, uri: str, test_client: FastAPITestHttpClient
) -> dict[str, Any]:
    """Create the given entity using an admin."""
    admin_client = get_client_for_admin(test_client)
    res = admin_client.post(f"{uri}", json=entity.model_dump())
    assert res.status_code == codes.OK
    return typing.cast(Dict[str, Any], res.json())


def admin_read_entity(
    entity_id: str, uri: str, test_client: FastAPITestHttpClient
) -> dict[str, Any]:
    """Get the given entity using an admin."""
    admin_client = get_client_for_admin(test_client)
    res = admin_client.get(f"{uri}/{entity_id}")
    assert res.status_code == codes.OK
    return typing.cast(Dict[str, Any], res.json())
