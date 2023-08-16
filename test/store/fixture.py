"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from collections.abc import Generator
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

import mlte.web.store.app_factory as app_factory
from mlte.artifact.model import ArtifactType
from mlte.store import StoreURI
from mlte.store.factory import create_store
from mlte.store.underlying.http import (
    ClientType,
    RemoteHttpStore,
    RemoteHttpStoreClient,
)
from mlte.store.underlying.memory import InMemoryStore
from mlte.store.underlying.fs import LocalFileSystemStore
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

_STORE_FIXTURE_NAMES = ["http_store", "memory_store", "fs_store"]


class TestclientCient(RemoteHttpStoreClient):
    def __init__(self, client: TestClient) -> None:
        super().__init__(ClientType.TESTCLIENT)

        self.client = client
        """The underlying client."""

    def get(self, url: str, **kwargs) -> httpx.Response:  # type: ignore[override]
        return self.client.get(url, **kwargs)

    def post(  # type: ignore[override]
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.post(url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:  # type: ignore[override]
        return self.client.delete(url, **kwargs)


@pytest.fixture(scope="function")
def http_store() -> RemoteHttpStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Configure the backing store
    state.set_store(create_store("memory://"))

    # Configure the application
    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Return a remote store that is able to hit the app
    client = TestClient(app)
    store = RemoteHttpStore(
        uri=StoreURI.from_string(str(client.base_url)),
        client=TestclientCient(client),
    )
    return store


@pytest.fixture(scope="function")
def memory_store() -> InMemoryStore:
    """A fixture for an in-memory store."""
    return InMemoryStore(StoreURI.from_string("memory://"))


@pytest.fixture(scope="function")
def fs_store(tmp_path) -> LocalFileSystemStore:
    """A fixture for an local FS store."""
    return LocalFileSystemStore(StoreURI.from_string(f"local://{tmp_path}"))


def stores() -> Generator[str, None, None]:
    """
    Yield store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name


def stores_and_types() -> Generator[tuple[str, ArtifactType], None, None]:
    """
    Yield store fixture names and artifact types to produce all combinations.
    :return: (store fixture name, artifact type)
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        for type in ArtifactType:
            yield store_fixture_name, type
