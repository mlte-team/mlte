"""Fixtures for MLTE custom list store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import List, Optional

import pytest
from sqlalchemy import StaticPool

from mlte.backend.core.config import settings
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel, CustomListModel
from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.http import HttpCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore
from mlte.store.custom_list.underlying.rdbs.store import RDBCustomListStore
from mlte.user.model import ResourceType, UserWithPassword
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import create_api_and_http_uri

CUSTOM_LIST_BASE_URI = f"{settings.API_PREFIX}/{ResourceType.CUSTOM_LIST.value}"
"""Base URI for custom lists."""

DEFAULT_LIST_NAME = CustomListName.QA_CATEGORIES
DEFAULT_ENTRY_NAME = "test_entry"
DEFAULT_ENTRY_DESCRIPTION = "test description"
DEFAULT_PARENT = None


def create_memory_store() -> InMemoryCustomListStore:
    return typing.cast(
        InMemoryCustomListStore,
        create_custom_list_store(
            StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
        ),
    )


def create_fs_store(path: Path) -> FileSystemCustomListStore:
    return typing.cast(
        FileSystemCustomListStore,
        create_custom_list_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


def create_rdbs_store() -> RDBCustomListStore:
    return RDBCustomListStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )


def create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpCustomListStore:
    """
    Get a HttpStore configured with test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(user)
    return HttpCustomListStore(uri=uri, client=client)


@pytest.fixture(scope="function")
def create_test_custom_list_store(
    tmpdir_factory,
) -> typing.Callable[[str], CustomListStore]:
    def _make(store_type) -> CustomListStore:
        if store_type == StoreType.REMOTE_HTTP:
            return create_api_and_http_store()
        elif store_type == StoreType.LOCAL_MEMORY:
            return create_memory_store()
        elif store_type == StoreType.LOCAL_FILESYSTEM:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_type == StoreType.RELATIONAL_DB:
            return create_rdbs_store()
        else:
            raise RuntimeError(f"Invalid store type received: {store_type}")

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
