"""
test/store/catalog/fixture.py

Fixtures for MLTE catalog store unit tests.
"""

from __future__ import annotations

import typing
from typing import Generator, Optional

import pytest

from mlte.store.base import StoreURIPrefix
from mlte.store.catalog.factory import create_store
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore

_STORE_FIXTURE_NAMES = ["memory_store"]

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryCatalogStore] = None
"""Global, initial, in memory store, cached for faster testing."""


def create_memory_store() -> InMemoryCatalogStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryCatalogStore, create_store(StoreURIPrefix.LOCAL_MEMORY[0])
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


@pytest.fixture(scope="function")
def memory_store() -> InMemoryCatalogStore:
    """A fixture for an in-memory store."""
    return create_memory_store()


def catalog_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name
