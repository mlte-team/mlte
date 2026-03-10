"""Fixtures for MLTE catalog store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

import pytest
from sqlalchemy import StaticPool

from mlte.backend.core.config import settings
from mlte.catalog.model import CatalogEntry, CatalogEntryHeader
from mlte.session.session_stores import SessionStores
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

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryCatalogStore] = None
"""Global, initial, in memory store, cached for faster testing."""

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


def create_rdbs_store(patched_create_engine) -> RelationalDBCatalogStore:
    """Creates a relational DB store."""
    with patched_create_engine():
        return RelationalDBCatalogStore(
            StoreURI.from_string(IN_MEMORY_SQLITE_DB),
            poolclass=StaticPool,
        )


def create_api_and_http_store(
    catalog_uris: dict[str, str] = {},
) -> HttpCatalogGroupStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(catalog_uris=catalog_uris)
    return HttpCatalogGroupStore(uri=uri, client=client)


@pytest.fixture(scope="function")
def create_test_catalog_store(
    patched_create_engine, tmpdir_factory, catalog_uris: dict[str, str] = {}
) -> typing.Callable[[StoreType, dict[str, str]], CatalogStore]:
    """Fixture to manually create a CustomList store."""

    def _make(
        store_type: StoreType, catalog_uris: dict[str, str] = catalog_uris
    ) -> CatalogStore:
        if store_type == StoreType.REMOTE_HTTP:
            return create_api_and_http_store(catalog_uris=catalog_uris)
        elif store_type == StoreType.LOCAL_MEMORY:
            return create_memory_store()
        elif store_type == StoreType.LOCAL_FILESYSTEM:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_type == StoreType.RELATIONAL_DB:
            return create_rdbs_store(patched_create_engine)

        else:
            raise RuntimeError(f"Invalid store type received: {store_type}")

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
    catalog_id: str = SessionStores.LOCAL_CATALOG_STORE_ID,
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
    catalog_id: str = SessionStores.LOCAL_CATALOG_STORE_ID,
) -> CatalogEntry:
    """Helper to get an entry structure."""
    entry = get_test_entry(id, description, code, catalog_id)

    if store_type == StoreType.REMOTE_HTTP:
        entry.header.identifier = (
            HTTPCatalogGroupEntryMapper.generate_composite_id(
                entry.header.catalog_id, entry.header.identifier
            )
        )

    return entry
