"""Fixtures for MLTE user store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

import pytest
from sqlalchemy.pool import StaticPool

from mlte.store.base import StoreType, StoreURI
from mlte.store.user.factory import create_user_store
from mlte.store.user.store import UserStore
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.http import HttpUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore
from mlte.user.model import UserWithPassword
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import create_api_and_http_uri

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryUserStore] = None
"""Global, initial, in memory store, cached for faster testing."""


def create_memory_store() -> InMemoryUserStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryUserStore,
            create_user_store(
                StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
            ),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def create_fs_store(path: Path) -> FileSystemUserStore:
    return typing.cast(
        FileSystemUserStore,
        create_user_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


def create_rdbs_store() -> RelationalDBUserStore:
    return RelationalDBUserStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpUserStore:
    """
    Get a HttpStore configured with test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(user)
    return HttpUserStore(uri=uri, client=client)


@pytest.fixture(scope="function")
def create_test_user_store(
    tmpdir_factory,
) -> typing.Callable[[str], UserStore]:
    def _make(store_type) -> UserStore:
        if store_type == StoreType.REMOTE_HTTP.value:
            return create_api_and_http_store()
        elif store_type == StoreType.LOCAL_MEMORY.value:
            return create_memory_store()
        elif store_type == StoreType.LOCAL_FILESYSTEM.value:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_type == StoreType.RELATIONAL_DB.value:
            return create_rdbs_store()
        else:
            raise RuntimeError(f"Invalid store type received: {store_type}")

    return _make
