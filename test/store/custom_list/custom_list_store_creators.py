"""
test/store/custom_list/custom_list_store_creators.py

Fixtures for MLTE custom list store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore


def create_fs_store(path: Path) -> FileSystemCustomListStore:
    return typing.cast(
        FileSystemCustomListStore,
        create_custom_list_store(
            f"{StoreURI.get_default_prefix(StoreType.LOCAL_FILESYSTEM)}{path}"
        ),
    )
