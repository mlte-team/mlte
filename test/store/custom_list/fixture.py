"""
test/store/custom_list/fixture.py

Fixtures for MLTE custom list store unit tests.
"""

from __future__ import annotations

import typing
from typing import Generator, List

import pytest

from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel, CustomListModel
from mlte.store.base import StoreType
from mlte.store.custom_list.store import CustomListStore
from test.store.custom_list.custom_list_store_creators import create_fs_store

DEFAULT_LIST_NAME = CustomListName.QA_CATEGORIES
DEFAULT_ENTRY_NAME = "test entry"
DEFAULT_ENTRY_DESCRIPTION = "test description"


def custom_list_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    # for store_fixture_name in StoreType:
    #     yield store_fixture_name.value
    yield StoreType.LOCAL_FILESYSTEM.value


@pytest.fixture(scope="function")
def create_test_store(
    tmpdir_factory,
) -> typing.Callable[[str], CustomListStore]:
    def _make(store_fixture_name) -> CustomListStore:
        if store_fixture_name == StoreType.LOCAL_FILESYSTEM.value:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

        # if store_fixture_name == StoreType.LOCAL_MEMORY.value:
        #     return create_memory_store()
        # elif store_fixture_name == StoreType.LOCAL_FILESYSTEM.value:
        #     return create_fs_store(tmpdir_factory.mktemp("data"))
        # elif store_fixture_name == StoreType.RELATIONAL_DB.value:
        #     return create_rdbs_store()
        #     pass
        # elif store_fixture_name == StoreType.REMOTE_HTTP.value:
        #     return create_api_and_http_store(catalog_id)
        #     pass
        # else:
        #     raise RuntimeError(
        #         f"Invalid store type received: {store_fixture_name}"
        #     )

    return _make


def get_test_list(
    name: CustomListName = DEFAULT_LIST_NAME,
    entries: List[CustomListEntryModel] = [],
) -> CustomListModel:
    """Helper to get a list structure."""
    return CustomListModel(name=name, entries=entries)


def get_test_entry(
    name: str = DEFAULT_ENTRY_NAME,
    description: str = DEFAULT_ENTRY_DESCRIPTION,
) -> CustomListEntryModel:
    """Helper to get a list entry structure."""
    return CustomListEntryModel(name=name, description=description)
