"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path

from sqlalchemy.pool import StaticPool

from mlte._private import url as url_utils
from mlte.store.artifact.factory import create_store
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBArtifactStore
from mlte.store.base import StoreURI, StoreURIPrefix
from mlte.store.common.http_clients import OAuthHttpClient, RequestsClient

FAKE_USER = "fake_user"
FAKE_PASS = "fake_pass"
FAKE_URI = "http://localhost:8080"
"""Default fake values for http store."""


def create_http_store(
    username: typing.Optional[str] = FAKE_USER,
    password: typing.Optional[str] = FAKE_PASS,
    uri: str = FAKE_URI,
    client: typing.Optional[OAuthHttpClient] = None,
) -> HttpArtifactStore:
    if client is None:
        client = RequestsClient(username, password)
    if username is None:
        username = FAKE_USER
    if password is None:
        password = FAKE_PASS
    return HttpArtifactStore(
        uri=StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        client=client,
    )


def create_memory_store() -> InMemoryStore:
    return typing.cast(
        InMemoryStore, create_store(StoreURIPrefix.LOCAL_MEMORY[0])
    )


def create_fs_store(tmp_path: Path) -> LocalFileSystemStore:
    return typing.cast(
        LocalFileSystemStore,
        create_store(f"{StoreURIPrefix.LOCAL_FILESYSTEM[1]}{tmp_path}"),
    )


def create_rdbs_store() -> RelationalDBArtifactStore:
    IN_MEMORY_SQLITE_DB = "sqlite+pysqlite:///:memory:"
    return RelationalDBArtifactStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )
