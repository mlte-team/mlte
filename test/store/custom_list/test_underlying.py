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
from mlte.custom_list.model import CustomListModel, CustomListEntryModel


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
def test_custom_list_entry(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """An custom list store supports custom list entry operations."""
    store: CustomListStore = create_test_store(store_fixture_name)
    
    test_list = get_test_list()
    test_entry = get_test_entry()
    new_description = "new_description"
    
    with ManagedCustomListSession(store.session()) as custom_list_store:
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