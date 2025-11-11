"""Fixtures for MLTE custom list store unit tests."""

from __future__ import annotations

import typing
from typing import Generator, List, Optional

import pytest

from mlte.backend.core.config import settings
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel, CustomListModel
from mlte.store.base import StoreType
from mlte.store.custom_list.store import CustomListStore
from mlte.user.model import ResourceType
from test.store.custom_list.custom_list_store_creators import (
    create_fs_store,
    create_http_store,
    create_memory_store,
    create_rdbs_store,
)

CUSTOM_LIST_BASE_URI = f"{settings.API_PREFIX}/{ResourceType.CUSTOM_LIST.value}"
"""Base URI for custom lists."""

DEFAULT_LIST_NAME = CustomListName.QA_CATEGORIES
DEFAULT_ENTRY_NAME = "test_entry"
DEFAULT_ENTRY_DESCRIPTION = "test description"
DEFAULT_PARENT = None


def custom_list_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in StoreType:
        yield store_fixture_name.value


@pytest.fixture(scope="function")
def create_test_store(
    tmpdir_factory,
) -> typing.Callable[[str], CustomListStore]:
    def _make(store_fixture_name) -> CustomListStore:
        if store_fixture_name == StoreType.REMOTE_HTTP.value:
            return create_http_store()
        elif store_fixture_name == StoreType.LOCAL_MEMORY.value:
            return create_memory_store()
        elif store_fixture_name == StoreType.LOCAL_FILESYSTEM.value:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_fixture_name == StoreType.RELATIONAL_DB.value:
            return create_rdbs_store()
        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

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
    parent: Optional[str] = DEFAULT_PARENT,
) -> CustomListEntryModel:
    """Helper to get a list entry structure."""
    return CustomListEntryModel(
        name=name, description=description, parent=parent
    )


def get_custom_list_uri(
    custom_list_id: Optional[str] = None,
    entry_id: Optional[str] = None,
    no_entry: bool = False,
):
    """Returns a proper URI for the endpoint based on the presence of the ids."""
    url = f"{CUSTOM_LIST_BASE_URI}"
    if custom_list_id is None:
        return f"{url}s"

    if no_entry:
        return f"{url}/{custom_list_id}"
    else:
        url = f"{url}/{custom_list_id}/entry"

    if entry_id is not None:
        url = f"{url}/{entry_id}"
    return url
