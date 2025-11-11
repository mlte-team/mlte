"""Fixtures for MLTE custom list store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

from sqlalchemy import StaticPool

from mlte._private import url as url_utils
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.custom_list.factory import create_custom_list_store
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.http import HttpCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore
from mlte.store.custom_list.underlying.rdbs.store import RDBCustomListStore
from test.store.defaults import IN_MEMORY_SQLITE_DB, get_http_defaults_if_needed


def create_http_store(
    username: Optional[str] = None,
    password: Optional[str] = None,
    uri: Optional[str] = None,
    client: Optional[OAuthHttpClient] = None,
) -> HttpCustomListStore:
    username, password, uri = get_http_defaults_if_needed(
        username, password, uri
    )
    return HttpCustomListStore(
        uri=StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        client=client,
    )


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
