"""
test/store/custom_list/test_underlying.py

Unit tests for the underlying custom list store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from test.store.custom_list.fixture import (  # noqa
    create_test_store,
    custom_list_stores,
    get_test_entry,
    get_test_list,
)

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
    """A custom list store supports custom list entry operations."""
    store: CustomListStore = create_test_store(store_fixture_name)

    test_list = get_test_list()
    test_entry = get_test_entry()
    new_description = "new description"
    new_parent = "new parent"

    with ManagedCustomListSession(store.session()) as custom_list_store:
        original_entries = custom_list_store.custom_list_entry_mapper.list(
            test_list.name
        )

        # Test creating an entry.
        custom_list_store.custom_list_entry_mapper.create(
            test_entry, test_list.name
        )
        read_entry = custom_list_store.custom_list_entry_mapper.read(
            test_entry.name, test_list.name
        )
        assert test_entry == read_entry

        # Test listing entries.
        entries = custom_list_store.custom_list_entry_mapper.list(
            test_list.name
        )
        assert len(entries) == 1 + len(original_entries)

        # Test editing an entry.
        test_entry.description = new_description
        test_entry.parent = new_parent
        _ = custom_list_store.custom_list_entry_mapper.edit(
            test_entry, test_list.name
        )
        read_entry = custom_list_store.custom_list_entry_mapper.read(
            test_entry.name, test_list.name
        )
        assert read_entry.description == new_description
        assert read_entry.parent == new_parent

        # Test deleting an entry.
        custom_list_store.custom_list_entry_mapper.delete(
            test_entry.name, test_list.name
        )
        with pytest.raises(errors.ErrorNotFound):
            custom_list_store.custom_list_entry_mapper.read(
                test_entry.name, test_list.name
            )

@pytest.mark.parametrize("store_fixture_name", custom_list_stores())
def test_custom_list_parent_mappings(
    store_fixture_name: str, create_test_store  # noqa
) -> None:
    """A custom list store properly handles parent relations."""
    store: CustomListStore = create_test_store(store_fixture_name)

    parent_list = CustomListName.QA_CATEGORIES
    child_list = CustomListName.QUALITY_ATTRIBUTES

    parent_name = "Test parent"
    parent = get_test_entry(name=parent_name, )
    child = get_test_entry(name="child", parent=parent_name)

    with ManagedCustomListSession(store.session()) as custom_list_store:
        custom_list_store.custom_list_entry_mapper.create(parent, parent_list)
        custom_list_store.custom_list_entry_mapper.create(child, child_list)
