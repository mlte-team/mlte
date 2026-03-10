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


def _create_memory_store() -> InMemoryUserStore:
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


def _create_fs_store(path: Path) -> FileSystemUserStore:
    return typing.cast(
        FileSystemUserStore,
        create_user_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


def _create_rdbs_store() -> RelationalDBUserStore:
    return RelationalDBUserStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def _create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpUserStore:
    """
    Get a HttpStore configured with test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(user)
    return HttpUserStore(uri=uri, client=client)


def _create_user_store(uri: str, tmpdir_factory) -> UserStore:
    """Function equivalent to the store's factory method, to be used for testing."""
    store_type = StoreURI.from_string(uri).type
    if store_type == StoreType.REMOTE_HTTP:
        return _create_api_and_http_store()
    elif store_type == StoreType.LOCAL_MEMORY:
        return _create_memory_store()
    elif store_type == StoreType.LOCAL_FILESYSTEM:
        return _create_fs_store(tmpdir_factory.mktemp("data"))
    elif store_type == StoreType.RELATIONAL_DB:
        return _create_rdbs_store()
    else:
        raise RuntimeError(f"Invalid store type received: {store_type}")


@pytest.fixture(scope="function")
def create_test_user_store(
    tmpdir_factory,
    patched_create_engine,
) -> typing.Callable[[StoreType], UserStore]:
    """Fixture used to manually create a test store."""

    def _make(store_type: StoreType) -> UserStore:
        """Internal function used to capture the tmpdir_factory fixture result."""
        with patched_create_engine():
            return _create_user_store(
                StoreURI.create_uri_string(store_type),
                tmpdir_factory,
            )

    return _make
