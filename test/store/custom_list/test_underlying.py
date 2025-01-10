"""
test/store/custom_list/test_underlying.py

Unit tests for the underlying custom list store implementations.
"""

import pytest

from typing import List

import mlte.store.error as errors
from mlte.store.custom_list.store import CustomListStore
from .fixture import (
    custom_list_stores
)
from test.store.custom_list.fixture import create_test_store, get_test_list, get_test_entry # noqa
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.custom_list.model import CustomList, CustomListEntry


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("store_fixture_name", custom_list_stores())
def test_init_store(store_fixture_name: str, create_test_store) -> None:  # noqa
    """A store can be initialized."""
    _ = create_test_store(store_fixture_name)

    # If we get here, the fixture was called and the store was initialized.
    assert True


@pytest.mark.parametrize("store_fixture_name", custom_list_stores())
def test_custom_list(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """An artifact store supports custom list entry operations."""
    store: CustomListStore = create_test_store(store_fixture_name)

    test_list = get_test_list()
    new_entries: List[CustomListEntry] = [
        CustomListEntry(name="new entry1", description="new description1"),
        CustomListEntry(name="new entry2", description="new description2"),
        CustomListEntry(name="new entry3", description="new description3")
    ]
    
    with ManagedCustomListSession(store.session()) as custom_list_store:
        original_lists = custom_list_store.custom_list_mapper.list()

        # Test creating a list.
        custom_list_store.custom_list_mapper.create(test_list)
        read_list = custom_list_store.custom_list_mapper.read(
            test_list.name
        )
        assert test_list == read_list

        # Test listing lists.
        lists = custom_list_store.custom_list_mapper.list()
        assert len(lists) == 1 + len(original_lists)

        # Test editing list.
        test_list.entries = new_entries
        _ = custom_list_store.custom_list_mapper.edit(test_list)
        read_list = custom_list_store.custom_list_mapper.read(
            test_list.name
        )
        assert read_list.entries == new_entries

        # Test deleting a list.
        custom_list_store.custom_list_mapper.delete(test_list.name)
        with pytest.raises(errors.ErrorNotFound):
            custom_list_store.custom_list_mapper.read(test_list.name)


@pytest.mark.parametrize("store_fixture_name", custom_list_stores())
def test_custom_list_entry(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """An custom list store supports custom list entry operations."""
    store: CustomListStore = create_test_store(store_fixture_name)

    test_list = get_test_list()

    test_entry = get_test_entry()
    new_description = "new_description"
    
    with ManagedCustomListSession(store.session()) as custom_list_store:
        # Adding a list for the entries to be added to
        custom_list_store.custom_list_mapper.create(test_list)

        original_entries = custom_list_store.custom_list_entry_mapper.list(test_list.name)

        # Test creating an entry.
        custom_list_store.custom_list_entry_mapper.create(test_list.name, test_entry)
        read_entry = custom_list_store.custom_list_entry_mapper.read(
            test_list.name, test_entry.name
        )
        assert test_entry == read_entry

        # Test listing entries.
        entries = custom_list_store.custom_list_entry_mapper.list(test_list.name)
        assert len(entries) == 1 + len(original_entries)

        # Test editing entry.
        test_entry.description = new_description
        _ = custom_list_store.custom_list_entry_mapper.edit(test_list.name, test_entry)
        read_entry = custom_list_store.custom_list_entry_mapper.read(
            test_list.name, test_entry.name
        )
        assert read_entry.description == new_description

        # Test deleting a list.
        custom_list_store.custom_list_entry_mapper.delete(test_list.name, test_entry.name)
        with pytest.raises(errors.ErrorNotFound):
            custom_list_store.custom_list_entry_mapper.read(test_list.name, test_entry.name)