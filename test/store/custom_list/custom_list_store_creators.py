"""Fixtures for MLTE custom list store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path

from sqlalchemy import StaticPool

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore
from mlte.store.custom_list.underlying.rdbs.store import RDBCustomListStore
from test.store.defaults import IN_MEMORY_SQLITE_DB


def create_memory_store() -> InMemoryCustomListStore:
    """Returns an in-memory store."""
    return typing.cast(
        InMemoryCustomListStore,
        create_custom_list_store(
            StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
        ),
    )


def create_fs_store(path: Path) -> FileSystemCustomListStore:
    return typing.cast(
        FileSystemCustomListStore,
        create_custom_list_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


def create_rdbs_store() -> RDBCustomListStore:
    return RDBCustomListStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )
