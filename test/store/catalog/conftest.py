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
from mlte.store.catalog import remote_catalog
from mlte.store.catalog.factory import create_catalog_store
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.http import (
    HttpCatalogGroupStore,
)
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore
from mlte.store.catalog.underlying.rdbs.store import RelationalDBCatalogStore
from mlte.store.constants import LOCAL_CATALOG_STORE_ID
from mlte.user.model import ResourceType
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import create_api_and_http_uri

CATALOG_BASE_URI = f"{settings.API_PREFIX}/{ResourceType.CATALOG.value}"
"""Base URI for catalogs."""

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryCatalogStore] = None
"""Global, initial, in memory store, cached for faster testing."""

DEFAULT_ENTRY_ID = "e1"
DEFAULT_ENTRY_DESC = "Code sample"
DEFAULT_ENTRY_CODE = "print('hello')"
TEST_CATALOG_ID = "cat1"
"""Default values."""


def _create_memory_store() -> InMemoryCatalogStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCatalogStore,
            create_catalog_store(StoreURI.from_type(StoreType.LOCAL_MEMORY)),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def _create_fs_store(tmp_path: Path) -> FileSystemCatalogStore:
    """Creates a file system store."""
    return typing.cast(
        FileSystemCatalogStore,
        create_catalog_store(
            StoreURI.from_type(StoreType.LOCAL_FILESYSTEM, str(tmp_path))
        ),
    )


def _create_rdbs_store() -> RelationalDBCatalogStore:
    """Creates a relational DB store."""
    return RelationalDBCatalogStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )


def _create_api_and_http_store(uri: StoreURI) -> HttpCatalogGroupStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(uri)
    return HttpCatalogGroupStore(uri=uri, client=client)


def _create_catalog_store(
    uri: StoreURI,
    catalog_id: str,
    tmpdir_factory,
) -> CatalogStore:
    """
    Function equivalent to the store's factory method, to be used for testing.
    It has catalog_id as a param to be a replacement patch for the actual catalog
    factory method, but it is not used for testing.
    """
    if uri.type == StoreType.REMOTE_HTTP:
        return _create_api_and_http_store(uri)
    elif uri.type == StoreType.LOCAL_MEMORY:
        return _create_memory_store()
    elif uri.type == StoreType.LOCAL_FILESYSTEM:
        return _create_fs_store(tmpdir_factory.mktemp("data"))
    elif uri.type == StoreType.RELATIONAL_DB:
        return _create_rdbs_store()

    else:
        raise RuntimeError(f"Invalid store type received: {uri}")


@pytest.fixture(scope="function")
def create_test_catalog_store(
    tmpdir_factory,
) -> typing.Callable[[StoreType], CatalogStore]:
    """Fixture to manually create a catalog store."""

    def _make(store_type: StoreType) -> CatalogStore:
        return _create_catalog_store(
            StoreURI.from_type(store_type),
            "",
            tmpdir_factory,
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
    catalog_id: str = LOCAL_CATALOG_STORE_ID,
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
    store_type: StoreType,
    id: str = DEFAULT_ENTRY_ID,
    description: str = DEFAULT_ENTRY_DESC,
    code: str = DEFAULT_ENTRY_CODE,
    catalog_id: str = LOCAL_CATALOG_STORE_ID,
    remote_catalog_id: str = LOCAL_CATALOG_STORE_ID,
) -> CatalogEntry:
    """Helper to get an entry structure."""
    entry = get_test_entry(id, description, code, catalog_id)

    if store_type == StoreType.REMOTE_HTTP:
        # When accessing a remote catalog, the id of the catalog in the remote server needs to be
        # set in the cataog_id variable, as well as a prefix in the entry id. The catalog_id variable is used
        # to set the remote catalog when creating/editing, and the entry id prefix when reading/deleting.
        entry.header.catalog_id = remote_catalog_id
        entry.header.identifier = remote_catalog.generate_composite_id(
            entry.header.catalog_id, entry.header.identifier
        )

    return entry
