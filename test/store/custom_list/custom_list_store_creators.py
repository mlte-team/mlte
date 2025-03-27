"""Fixtures for MLTE custom list store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore


def create_memory_store() -> InMemoryCustomListStore:
    """Returns an in-memory store."""
    return typing.cast(
        InMemoryCustomListStore,
        create_custom_list_store(
            f"{StoreURI.get_default_prefix(StoreType.LOCAL_MEMORY)}"
        ),
    )


def create_fs_store(path: Path) -> FileSystemCustomListStore:
    return typing.cast(
        FileSystemCustomListStore,
        create_custom_list_store(
            f"{StoreURI.get_default_prefix(StoreType.LOCAL_FILESYSTEM)}{path}"
        ),
    )
