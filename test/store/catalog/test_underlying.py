"""
test/store/catalog/test_underlying.py

Unit tests for the underlying catalog store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.catalog.model import (
    CatalogEntry,
    CatalogEntryHeader,
    CatalogEntryType,
)
from mlte.store.catalog.store import CatalogStore, ManagedCatalogSession

from .fixture import catalog_stores, create_memory_store, memory_store  # noqa

TEST_MOD_ID = "mod1"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_test_entry() -> CatalogEntry:
    """Helper to get an entry structure."""
    id = "e1"
    description = "code sample"
    code = "print(`hello`)"
    header = CatalogEntryHeader(identifier=id)
    test_entry = CatalogEntry(
        header=header,
        code=code,
        description=description,
        code_type=CatalogEntryType.MEASUREMENT,
    )
    return test_entry


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = create_memory_store()


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_catalog_entry(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports catalog entry operations."""
    store: CatalogStore = request.getfixturevalue(store_fixture_name)

    test_entry = get_test_entry()
    description2 = "short code sample"

    with ManagedCatalogSession(store.session()) as catalog_store:
        original_entries = catalog_store.entry_mapper.list()

        # Test creating an entry.
        catalog_store.entry_mapper.create(test_entry)
        read_entry = catalog_store.entry_mapper.read(
            test_entry.header.identifier
        )
        assert test_entry == read_entry

        # Test listing entries.
        entries = catalog_store.entry_mapper.list()
        assert len(entries) == 1 + len(original_entries)

        # Test editing all entry info.
        test_entry.description = description2
        _ = catalog_store.entry_mapper.edit(test_entry)
        read_entry = catalog_store.entry_mapper.read(
            test_entry.header.identifier
        )
        assert read_entry.description == description2

        # Test deleting an entry.
        catalog_store.entry_mapper.delete(test_entry.header.identifier)
        with pytest.raises(errors.ErrorNotFound):
            catalog_store.entry_mapper.read(test_entry.header.identifier)
