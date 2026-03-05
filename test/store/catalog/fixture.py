"""Fixtures for MLTE catalog store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

import pytest
from sqlalchemy import StaticPool

from mlte.backend.core.config import settings
from mlte.catalog.model import CatalogEntry, CatalogEntryHeader
from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.factory import create_catalog_store
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.http import (
    HTTPCatalogGroupEntryMapper,
    HttpCatalogGroupStore,
)
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore
from mlte.store.catalog.underlying.rdbs.store import RelationalDBCatalogStore
from mlte.user.model import ResourceType
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import create_api_and_http_uri

CATALOG_BASE_URI = f"{settings.API_PREFIX}/{ResourceType.CATALOG.value}"
"""Base URI for catalogs."""

DEFAULT_ENTRY_ID = "e1"
DEFAULT_ENTRY_DESC = "Code sample"
DEFAULT_ENTRY_CODE = "print('hello')"
TEST_CATALOG_ID = "cat1"
"""Default values."""


def create_memory_store() -> InMemoryCatalogStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCatalogStore,
            create_catalog_store(
                StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
            ),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def create_fs_store(tmp_path: Path) -> FileSystemCatalogStore:
    """Creates a file system store."""
    return typing.cast(
        FileSystemCatalogStore,
        create_catalog_store(
            StoreURI.create_uri_string(
                StoreType.LOCAL_FILESYSTEM, str(tmp_path)
            )
        ),
    )


def create_rdbs_store() -> RelationalDBCatalogStore:
    """Creates a relational DB store."""
    return RelationalDBCatalogStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )


def create_api_and_http_store(
    catalog_id: str = TEST_CATALOG_ID,
) -> HttpCatalogGroupStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(default_catalog_id=catalog_id)
    return HttpCatalogGroupStore(uri=uri, client=client)


@pytest.fixture(scope="function")
def create_test_store(
    tmpdir_factory, test_catalog_id: str = TEST_CATALOG_ID
) -> typing.Callable[[str], CatalogStore]:
    def _make(
        store_fixture_name, catalog_id: str = test_catalog_id
    ) -> CatalogStore:
        if store_fixture_name == StoreType.REMOTE_HTTP.value:
            return create_api_and_http_store(catalog_id)
        elif store_fixture_name == StoreType.LOCAL_MEMORY.value:
            return create_memory_store()
        elif store_fixture_name == StoreType.LOCAL_FILESYSTEM.value:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_fixture_name == StoreType.RELATIONAL_DB.value:
            return create_rdbs_store()

        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

    return _make


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_entry_uri(
    catalog_id: Optional[str] = None,
    entry_id: Optional[str] = None,
    only_base: bool = False,
):
    """Returns a proper URI for the endpoint based on the presence of the ids."""
    url = f"{CATALOG_BASE_URI}"
    if only_base:
        return f"{url}s"

    if catalog_id is None:
        url = f"{url}s/entry"
    else:
        url = f"{url}/{catalog_id}/entry"
        if entry_id is not None:
            url = f"{url}/{entry_id}"
    return url


def get_test_entry(
    id: str = DEFAULT_ENTRY_ID,
    description: str = DEFAULT_ENTRY_DESC,
    code: str = DEFAULT_ENTRY_CODE,
    catalog_id: str = TEST_CATALOG_ID,
    creator: Optional[str] = None,
    updater: Optional[str] = None,
) -> CatalogEntry:
    """Helper to get an entry structure."""
    id = id
    description = description
    code = code
    header = CatalogEntryHeader(
        identifier=id, catalog_id=catalog_id, creator=creator, updater=updater
    )
    test_entry = CatalogEntry(
        header=header,
        code=code,
        description=description,
    )

    return test_entry


def get_test_entry_for_store(
    id: str = DEFAULT_ENTRY_ID,
    description: str = DEFAULT_ENTRY_DESC,
    code: str = DEFAULT_ENTRY_CODE,
    catalog_id: str = TEST_CATALOG_ID,
    store_name: str = "",
) -> CatalogEntry:
    """Helper to get an entry structure."""
    entry = get_test_entry(id, description, code, catalog_id)

    if store_name == StoreType.REMOTE_HTTP.value:
        entry.header.identifier = (
            HTTPCatalogGroupEntryMapper.generate_composite_id(
                entry.header.catalog_id, entry.header.identifier
            )
        )

    return entry
