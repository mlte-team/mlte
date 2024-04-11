"""
test/backend/fixture/http.py

Fixtures for artifact store HTTP unit tests.
"""

from __future__ import annotations

from typing import Any, Generator, Optional, Tuple

import httpx
import pytest
from fastapi.testclient import TestClient

import test.backend.fixture.api as api_helpers
from mlte.artifact.type import ArtifactType
from mlte.backend.core.config import settings
from mlte.store.common.http_clients import HttpClientType, OAuthHttpClient

"""
This list contains the global collection of test clients.
However, because we cannot directly parametrize a test with
a fixture function, we specify via strings and then use the
`request` fixture to translate this into the actual fixture.
"""
_CLIENTS = ["mem_store_and_test_http_client"]

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
def mem_store_and_test_http_client() -> FastAPITestHttpClient:
    """Sets up memory based store for the API and gets an associated client."""
    return setup_API_and_test_client()


def setup_API_and_test_client() -> FastAPITestHttpClient:
    """
    Configure API for memory stores and return a test HTTP client.
    :return: The client
    """
    # Setup API, configure to use memory artifact store and create app itself.
    app = api_helpers.setup_api_with_mem_stores()

    # Create the test client, and authenticate to get token and allow protected endpoints to work.
    client = FastAPITestHttpClient(TestClient(app))
    client.username = api_helpers.TEST_API_USER
    client.password = api_helpers.TEST_API_PASS
    client.authenticate(f"{settings.API_PREFIX}")
    return client


def clients() -> Generator[str, None, None]:
    """
    Yield test clients.
    :return: A test client configured for backend
    """
    for client in _CLIENTS:
        yield client


def clients_and_types() -> Generator[Tuple[str, ArtifactType], None, None]:
    """
    Yield test clients and artifact types to produce all combinations.
    :return: (test client configured for backend, artifact type)
    """
    for client in _CLIENTS:
        for type in ArtifactType:
            yield client, type
