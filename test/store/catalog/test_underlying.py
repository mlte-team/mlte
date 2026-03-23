"""Unit tests for the underlying catalog store implementations."""

from typing import Callable

import pytest

import mlte.store.error as errors
from mlte.store.base import StoreType
from mlte.store.catalog import remote_catalog
from mlte.store.catalog.catalog_group import (
    CatalogStoreGroup,
    ManagedCatalogGroupSession,
)
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.store_session import ManagedCatalogSession
from mlte.store.query import Query
from test.store.catalog.conftest import get_test_entry_for_store
from test.store.utils import store_types

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def create_store_with_mem_cat(
    create_test_catalog_store,
    store_type: StoreType,
) -> CatalogStore:
    """Creates a catalog store with an in mem catalog."""
    store: CatalogStore = create_test_catalog_store(store_type)
    return store


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_type", store_types())
def test_init_store(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A store can be initialized."""
    _ = create_test_catalog_store(store_type)

    # If we get here, the fixture was called and the store was initialized.
    assert True


@pytest.mark.parametrize("store_type", store_types())
def test_catalog_entry(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A catalog store supports catalog entry operations."""
    store = create_test_catalog_store(store_type)

    test_entry = get_test_entry_for_store(store_type=store_type)
    description2 = "short code sample"

    with ManagedCatalogSession(store.session()) as catalog_store:
        original_entries = catalog_store.entry_mapper.list()

        # Test creating an entry.
        catalog_store.entry_mapper.create(test_entry)
        read_entry = catalog_store.entry_mapper.read(
            test_entry.header.identifier
        )
        read_entry.header.creator = None  # To avoid issue with creator.
        read_entry.header.created = -1  # To avoid issue with creation time.

        if store_type == StoreType.REMOTE_HTTP:
            clean_test_entry = remote_catalog.remove_remote_catalog_id(
                test_entry
            )
            assert clean_test_entry == read_entry
        else:
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


@pytest.mark.parametrize("store_type", store_types())
def test_catalog_group(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A catalog store group supports general operations."""
    if store_type == StoreType.REMOTE_HTTP:
        # NOTE: MLTE does not support having 2 separate TestAPIs at the same time,
        # as there is one global shared state that they access and overwrite.
        # Thus, two HTTP stores, which require two TestAPIs, won't work properly.
        pytest.skip()

    store1_id = "st1"
    store2_id = "st2"
    store1: CatalogStore = create_test_catalog_store(store_type)
    store2: CatalogStore = create_test_catalog_store(store_type)

    store_group = CatalogStoreGroup()
    store_group.add_catalog(store1_id, store1)
    store_group.add_catalog(store2_id, store2)

    test_entry1 = get_test_entry_for_store(
        id="ce1", store_type=store_type, catalog_id=store1_id
    )
    test_entry2 = get_test_entry_for_store(
        id="ce2", store_type=store_type, catalog_id=store2_id
    )

    with ManagedCatalogGroupSession(store_group.session()) as group_session:
        group_session.sessions[store1_id].entry_mapper.create(test_entry1)
        group_session.sessions[store2_id].entry_mapper.create(test_entry2)

        # Test listing entries.
        entries = group_session.list_details()
        assert len(entries) == 2

        # Test searching entries.
        entries = group_session.search()
        assert len(entries) == 2


@pytest.mark.parametrize("store_type", store_types())
def test_list_details(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A catalog store store supports list queries."""
    store = create_test_catalog_store(store_type)

    with ManagedCatalogSession(store.session()) as session:
        original_entries = session.entry_mapper.list_details()
        original_len = len(original_entries)

        e0 = get_test_entry_for_store(
            id="e1",
            description="code 1",
            code="print nothing",
            store_type=store_type,
        )
        e1 = get_test_entry_for_store(
            id="e2",
            description="code 1",
            code="print nothing",
            store_type=store_type,
        )

        for entry in [e0, e1]:
            session.entry_mapper.create(entry)

        entries = session.entry_mapper.list_details()
        assert len(entries) == original_len + 2


@pytest.mark.parametrize("store_type", store_types())
def test_search(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A catalog store store supports queries."""
    store = create_test_catalog_store(store_type)

    with ManagedCatalogSession(store.session()) as session:
        original_entries = session.entry_mapper.list_details()
        original_len = len(original_entries)

        e0 = get_test_entry_for_store(
            id="e1",
            description="code 1",
            code="print nothing",
            store_type=store_type,
        )
        e1 = get_test_entry_for_store(
            id="e2",
            description="code 1",
            code="print nothing",
            store_type=store_type,
        )

        for entry in [e0, e1]:
            session.entry_mapper.create(entry)

        query = Query()
        entries = session.entry_mapper.search(query)
        assert len(entries) == original_len + 2


@pytest.mark.parametrize("store_type", store_types())
def test_invalid_chars(
    store_type: StoreType,
    create_test_catalog_store: Callable[[StoreType], CatalogStore],
) -> None:
    """A catalog store store supports invalid storage chars."""
    remote_catalog_id = "weird/catalog_id"
    store = create_test_catalog_store(store_type)

    entry_id = "weird/name"
    test_entry = get_test_entry_for_store(
        store_type=store_type, id=entry_id, catalog_id=remote_catalog_id
    )

    with ManagedCatalogSession(store.session()) as catalog_store:
        # Test creating an entry.
        catalog_store.entry_mapper.create(test_entry)
        read_entry = catalog_store.entry_mapper.read(
            test_entry.header.identifier
        )
        read_entry.header.creator = None  # To avoid issue with creator.
        read_entry.header.created = -1  # To avoid issue with creation time.
        if store_type == StoreType.REMOTE_HTTP:
            test_entry = remote_catalog.remove_remote_catalog_id(test_entry)
        assert test_entry == read_entry
