"""
test/store/catalog/fixture.py

Fixtures for MLTE catalog store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Generator, Optional

import pytest
from sqlalchemy import StaticPool

from mlte._private import url as url_utils
from mlte.store.base import StoreURI, StoreURIPrefix
from mlte.store.catalog.factory import create_store
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.http import HttpCatalogStore
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore
from mlte.store.catalog.underlying.rdbs.store import RelationalDBCatalogStore
from mlte.store.common.http_clients import RequestsClient
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI

FAKE_USER = "fake_user"
FAKE_PASS = "fake_pass"
FAKE_URI = "http://localhost:8080"

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryCatalogStore] = None
"""Global, initial, in memory store, cached for faster testing."""

_STORE_FIXTURE_NAMES = ["memory_store", "fs_store", "rdbs_store"]


def catalog_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name


def create_memory_store() -> InMemoryCatalogStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCatalogStore, create_store(StoreURIPrefix.LOCAL_MEMORY[0])
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def create_fs_store(tmp_path: Path) -> FileSystemCatalogStore:
    """Creates a file system store."""
    return typing.cast(
        FileSystemCatalogStore,
        create_store(f"{StoreURIPrefix.LOCAL_FILESYSTEM[1]}{tmp_path}"),
    )


def create_rdbs_store() -> RelationalDBCatalogStore:
    """Creates a relational DB store."""
    IN_MEMORY_SQLITE_DB = "sqlite+pysqlite:///:memory:"
    return RelationalDBCatalogStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )


def create_http_store() -> HttpCatalogStore:
    """
    Get a HttpCatalogStore configured with a test client.
    :return: The configured store
    """
    # Set an in memory store and get a test http client, configured for the app.
    user = user_generator.build_admin_user()
    test_api = TestAPI()
    test_api.set_users(user)
    client = test_api.get_test_client()

    username = client.username if client.username else FAKE_USER
    password = client.password if client.password else FAKE_PASS
    uri = str(client.client.base_url)
    return HttpCatalogStore(
        StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        RequestsClient(username, password),
    )


@pytest.fixture(scope="function")
def create_test_store(tmpdir_factory) -> typing.Callable[[str], CatalogStore]:
    def _make(store_fixture_name) -> CatalogStore:
        if store_fixture_name == "memory_store":
            return create_memory_store()
        elif store_fixture_name == "fs_store":
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_fixture_name == "rdbs_store":
            return create_rdbs_store()
        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

    return _make
