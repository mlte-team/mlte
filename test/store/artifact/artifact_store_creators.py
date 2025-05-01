"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing
from pathlib import Path

from sqlalchemy.pool import StaticPool

from mlte._private import url as url_utils
from mlte.store.artifact.factory import create_artifact_store
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBArtifactStore
from mlte.store.base import StoreType, StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from test.store.defaults import IN_MEMORY_SQLITE_DB, get_http_defaults_if_needed


def create_http_store(
    username: typing.Optional[str] = None,
    password: typing.Optional[str] = None,
    uri: typing.Optional[str] = None,
    client: typing.Optional[OAuthHttpClient] = None,
) -> HttpArtifactStore:
    username, password, uri = get_http_defaults_if_needed(
        username, password, uri
    )
    return HttpArtifactStore(
        uri=StoreURI.from_string(
            url_utils.set_url_username_password(uri, username, password)
        ),
        client=client,
    )


def create_memory_store() -> InMemoryStore:
    return typing.cast(
        InMemoryStore,
        create_artifact_store(
            StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
        ),
    )


def create_fs_store(tmp_path: Path) -> LocalFileSystemStore:
    return typing.cast(
        LocalFileSystemStore,
        create_artifact_store(
            StoreURI.create_uri_string(
                StoreType.LOCAL_FILESYSTEM, str(tmp_path)
            )
        ),
    )


def create_rdbs_store() -> RelationalDBArtifactStore:
    return RelationalDBArtifactStore(
        StoreURI.from_string(IN_MEMORY_SQLITE_DB),
        poolclass=StaticPool,
    )
