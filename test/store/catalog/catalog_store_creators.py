"""
test/store/catalog/catalog_store_creators.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

from sqlalchemy import StaticPool

from mlte._private import url as url_utils
from mlte.store.base import StoreURI, StoreURIPrefix
from mlte.store.catalog.factory import create_catalog_store
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.http import HttpCatalogGroupStore
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore
from mlte.store.catalog.underlying.rdbs.store import RelationalDBCatalogStore
from mlte.store.common.http_clients import OAuthHttpClient
from test.store.defaults import IN_MEMORY_SQLITE_DB, get_http_defaults_if_needed

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryCatalogStore] = None
"""Global, initial, in memory store, cached for faster testing."""


def create_memory_store() -> InMemoryCatalogStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCatalogStore,
            create_catalog_store(StoreURIPrefix.LOCAL_MEMORY[0]),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def create_fs_store(tmp_path: Path) -> FileSystemCatalogStore:
    """Creates a file system store."""
    return typing.cast(
        FileSystemCatalogStore,
        create_catalog_store(f"{StoreURIPrefix.LOCAL_FILESYSTEM[1]}{tmp_path}"),
    )


def create_rdbs_store() -> RelationalDBCatalogStore:
    """Creates a relational DB store."""
    return RelationalDBCatalogStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )


def create_http_store(
    username: Optional[str] = None,
    password: Optional[str] = None,
    uri: Optional[str] = None,
    client: Optional[OAuthHttpClient] = None,
) -> HttpCatalogGroupStore:
    username, password, uri = get_http_defaults_if_needed(
        username, password, uri
    )
    return HttpCatalogGroupStore(
        uri=StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        client=client,
    )
