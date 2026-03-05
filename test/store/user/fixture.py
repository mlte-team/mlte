"""Fixtures for MLTE user store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Optional

import pytest
from sqlalchemy.pool import StaticPool

from mlte._private import url as url_utils
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.user.factory import create_user_store
from mlte.store.user.store import UserStore
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.http import HttpUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore
from mlte.user.model import UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.defaults import IN_MEMORY_SQLITE_DB, get_http_defaults_if_needed

CACHED_DEFAULT_MEMORY_STORE: Optional[InMemoryUserStore] = None
"""Global, initial, in memory store, cached for faster testing."""


def create_memory_store() -> InMemoryUserStore:
    """Returns an in-memory store. Caches an initialized one to make testing faster."""
    global CACHED_DEFAULT_MEMORY_STORE
    if CACHED_DEFAULT_MEMORY_STORE is None:
        CACHED_DEFAULT_MEMORY_STORE = typing.cast(
            InMemoryUserStore,
            create_user_store(
                StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
            ),
        )

    return CACHED_DEFAULT_MEMORY_STORE.clone()


def create_fs_store(path: Path) -> FileSystemUserStore:
    return typing.cast(
        FileSystemUserStore,
        create_user_store(
            StoreURI.create_uri_string(StoreType.LOCAL_FILESYSTEM, str(path))
        ),
    )


def create_rdbs_store() -> RelationalDBUserStore:
    return RelationalDBUserStore(
        uri=StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


def create_http_store(
    username: Optional[str] = None,
    password: Optional[str] = None,
    uri: Optional[str] = None,
    client: Optional[OAuthHttpClient] = None,
) -> HttpUserStore:
    username, password, uri = get_http_defaults_if_needed(
        username, password, uri
    )
    return HttpUserStore(
        uri=StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        client=client,
    )


def create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpUserStore:
    """
    Get a HttpStore configured with test client.
    :return: The configured store
    """
    user = user_generator.build_admin_user()
    test_api = TestAPI(user=user)
    client = test_api.get_test_client()

    return create_http_store(
        username=client.username,
        password=client.password,
        uri=str(client.client.base_url),
        client=client,
    )


@pytest.fixture(scope="function")
def create_test_user_store(
    tmpdir_factory,
) -> typing.Callable[[str], UserStore]:
    def _make(store_type) -> UserStore:
        if store_type == StoreType.REMOTE_HTTP.value:
            return create_api_and_http_store()
        elif store_type == StoreType.LOCAL_MEMORY.value:
            return create_memory_store()
        elif store_type == StoreType.LOCAL_FILESYSTEM.value:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_type == StoreType.RELATIONAL_DB.value:
            return create_rdbs_store()
        else:
            raise RuntimeError(f"Invalid store type received: {store_type}")

    return _make
