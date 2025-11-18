"""
test/store/user/fixture.py

Fixtures for MLTE user store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Generator, Optional

import pytest
from sqlalchemy.pool import StaticPool

from mlte.store.base import StoreType, StoreURI
from mlte.store.user.factory import create_user_store
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore
from test.store.defaults import IN_MEMORY_SQLITE_DB

_STORE_FIXTURE_NAMES = ["memory_store", "rdbs_store", "fs_store"]

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


@pytest.fixture(scope="function")
def memory_store() -> InMemoryUserStore:
    """A fixture for an in-memory store."""
    return create_memory_store()


def create_fs_store(path: Path) -> FileSystemUserStore:
    return typing.cast(
        FileSystemUserStore,
        create_user_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


@pytest.fixture(scope="function")
def fs_store(tmp_path) -> FileSystemUserStore:
    """A fixture for an local FS store."""
    return create_fs_store(tmp_path)


def create_rdbs_store() -> RelationalDBUserStore:
    return RelationalDBUserStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="function")
def rdbs_store() -> RelationalDBUserStore:
    """A fixture for an in-memory RDBS store."""
    return create_rdbs_store()


def user_stores() -> Generator[str, None, None]:
    """
    Yield User store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name
