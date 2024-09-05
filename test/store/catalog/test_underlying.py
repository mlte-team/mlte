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
from mlte.store.catalog.catalog_group import (
    CatalogStoreGroup,
    ManagedCatalogGroupSession,
)
from mlte.store.catalog.store import CatalogStore, ManagedCatalogSession
from mlte.store.catalog.underlying.http import HTTPCatalogGroupEntryMapper
from mlte.store.query import Query
from test.store.catalog.catalog_store_creators import (  # noqa
    create_fs_store,
    create_http_store,
    create_memory_store,
    create_rdbs_store,
)
from test.store.catalog.fixture import create_test_store  # noqa
from test.store.catalog.fixture import TEST_CATALOG_ID, catalog_stores

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_test_entry(
    id: str = "e1",
    description: str = "code sample",
    code: str = "print('hello')",
    catalog_id="cat1",
    store_fixture_name: str = "",
) -> CatalogEntry:
    """Helper to get an entry structure."""
    id = id
    description = description
    code = code
    header = CatalogEntryHeader(identifier=id, catalog_id=catalog_id)
    test_entry = CatalogEntry(
        header=header,
        code=code,
        description=description,
        code_type=CatalogEntryType.MEASUREMENT,
    )

    if store_fixture_name == "http_store":
        test_entry.header.catalog_id = TEST_CATALOG_ID
        test_entry.header.identifier = (
            HTTPCatalogGroupEntryMapper.generate_composite_id(
                TEST_CATALOG_ID, test_entry.header.identifier
            )
        )

    return test_entry


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_init_store(store_fixture_name: str, create_test_store) -> None:  # noqa
    """A store can be initialized."""
    _ = create_test_store(store_fixture_name)

    # If we get here, the fixture was called and the store was initialized.
    assert True


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_catalog_entry(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """An artifact store supports catalog entry operations."""
    store: CatalogStore = create_test_store(store_fixture_name)

    test_entry = get_test_entry(store_fixture_name=store_fixture_name)
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


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_catalog_group(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """A catalog store group supports general operations."""
    store1: CatalogStore = create_test_store(store_fixture_name)
    store2: CatalogStore = create_test_store(store_fixture_name)

    store1_id = "st1"
    store2_id = "st2"
    store_group = CatalogStoreGroup()
    store_group.add_catalog(store1_id, store1)
    store_group.add_catalog(store2_id, store2)

    test_entry1 = get_test_entry(
        id="ce1", store_fixture_name=store_fixture_name
    )
    test_entry2 = get_test_entry(
        id="ce2", store_fixture_name=store_fixture_name
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


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_list_details(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """A catalog store store supports queries."""
    store: CatalogStore = create_test_store(store_fixture_name)

    with ManagedCatalogSession(store.session()) as session:
        e0 = get_test_entry(
            id="e1",
            description="code 1",
            code="print nothing",
            store_fixture_name=store_fixture_name,
        )
        e1 = get_test_entry(
            id="e2",
            description="code 1",
            code="print nothing",
            store_fixture_name=store_fixture_name,
        )

        for entry in [e0, e1]:
            session.entry_mapper.create(entry)

        entries = session.entry_mapper.list_details()
        assert len(entries) == 2


@pytest.mark.parametrize("store_fixture_name", catalog_stores())
def test_search(store_fixture_name: str, create_test_store) -> None:  # noqa
    """A catalog store store supports queries."""
    store: CatalogStore = create_test_store(store_fixture_name)

    with ManagedCatalogSession(store.session()) as session:
        e0 = get_test_entry(
            id="e1",
            description="code 1",
            code="print nothing",
            store_fixture_name=store_fixture_name,
        )
        e1 = get_test_entry(
            id="e2",
            description="code 1",
            code="print nothing",
            store_fixture_name=store_fixture_name,
        )

        for entry in [e0, e1]:
            session.entry_mapper.create(entry)

        query = Query()
        entries = session.entry_mapper.search(query)
        assert len(entries) == 2
