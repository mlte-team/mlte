"""
test/store/custom_list/custom_list_store_creators.py

Fixtures for MLTE custom list store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore

CACHED_DEFAULT_MEMORY_STORE : Optional[InMemoryCustomListStore] = None
"""Global, initial, in memory store, cached for faster testing."""


def create_memory_store() -> InMemoryCustomListStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCustomListStore,
            create_custom_list_store(
                f"{StoreURI.get_default_prefix(StoreType.LOCAL_MEMORY)}"
            ),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()

def create_fs_store(path: Path) -> FileSystemCustomListStore:
    return typing.cast(
        FileSystemCustomListStore,
        create_custom_list_store(
            f"{StoreURI.get_default_prefix(StoreType.LOCAL_FILESYSTEM)}{path}"
        ),
    )
