"""
test/store/catalog/fixture.py

Fixtures for MLTE catalog store unit tests.
"""

from __future__ import annotations

import typing
from typing import Generator

import pytest

from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.http import HttpCatalogGroupStore
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.catalog.catalog_store_creators import (
    create_fs_store,
    create_http_store,
    create_memory_store,
    create_rdbs_store,
)

TEST_CATALOG_ID = "cat1"
"""Default test catalog."""

_STORE_FIXTURE_NAMES = ["memory_store", "fs_store", "rdbs_store", "http_store"]


def catalog_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name


def create_api_and_http_store() -> HttpCatalogGroupStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Set an in memory store and get a test http client, configured for the app.
    user = user_generator.build_admin_user()
    test_api = TestAPI(user=user)
    client = test_api.get_test_client()

    return create_http_store(
        username=client.username,
        password=client.password,
        uri=str(client.client.base_url),
        client=client,
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
        elif store_fixture_name == "http_store":
            return create_api_and_http_store()
        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

    return _make
