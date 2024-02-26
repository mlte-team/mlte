"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing
from typing import Any, Generator, Tuple

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

import mlte.web.store.app_factory as app_factory
from mlte.artifact.type import ArtifactType
from mlte.store.artifact.factory import create_store
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import (
    ClientType,
    RemoteHttpStore,
    RemoteHttpStoreClient,
)
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBStore
from mlte.store.base import StoreURI
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

_STORE_FIXTURE_NAMES = ["http_store", "memory_store", "fs_store", "rdbs_store"]


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
    state.set_store(create_memory_store())

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


def create_memory_store() -> InMemoryStore:
    return typing.cast(InMemoryStore, create_store("memory://"))


@pytest.fixture(scope="function")
def memory_store() -> InMemoryStore:
    """A fixture for an in-memory store."""
    return create_memory_store()


def create_fs_store(tmp_path) -> LocalFileSystemStore:
    return typing.cast(
        LocalFileSystemStore, create_store(f"local://{tmp_path}")
    )


@pytest.fixture(scope="function")
def fs_store(tmp_path) -> LocalFileSystemStore:
    """A fixture for an local FS store."""
    return create_fs_store(tmp_path)


def create_rdbs_store() -> RelationalDBStore:
    return RelationalDBStore(
        StoreURI.from_string("sqlite+pysqlite:///:memory:"),
        poolclass=StaticPool,
    )


@pytest.fixture(scope="function")
def rdbs_store() -> RelationalDBStore:
    """A fixture for an in-memory RDBS store."""
    return create_rdbs_store()


def stores() -> Generator[str, None, None]:
    """
    Yield store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name


def stores_and_types() -> Generator[Tuple[str, ArtifactType, bool], None, None]:
    """
    Yield store fixture names and artifact types to produce all combinations.
    :return: (store fixture name, artifact type)
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        for type in ArtifactType:
            for complete in [False, True]:
                yield store_fixture_name, type, complete
