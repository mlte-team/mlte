"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing

from sqlalchemy.pool import StaticPool

from mlte.store.artifact.factory import create_store
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBStore
from mlte.store.base import StoreURI, StoreURIPrefix


def create_memory_store() -> InMemoryStore:
    return typing.cast(
        InMemoryStore, create_store(StoreURIPrefix.LOCAL_MEMORY[0])
    )


def create_fs_store(tmp_path) -> LocalFileSystemStore:
    return typing.cast(
        LocalFileSystemStore,
        create_store(f"{StoreURIPrefix.LOCAL_FILESYSTEM[1]}{tmp_path}"),
    )


def create_rdbs_store() -> RelationalDBStore:
    IN_MEMORY_SQLITE_DB = "sqlite+pysqlite:///:memory:"
    return RelationalDBStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )
