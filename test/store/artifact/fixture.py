"""Fixtures for MLTE artifact store unit tests."""

from __future__ import annotations

import typing
from pathlib import Path
from typing import Generator, Optional, Tuple

import pytest
from sqlalchemy import StaticPool

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.context.model import Model, Version
from mlte.store.artifact.factory import create_artifact_store
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBArtifactStore
from mlte.store.base import StoreType, StoreURI
from mlte.user.model import UserWithPassword
from test.store.defaults import IN_MEMORY_SQLITE_DB
from test.store.utils import create_api_and_http_uri


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


def create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpArtifactStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    client, uri = create_api_and_http_uri(user)
    return HttpArtifactStore(uri=uri, client=client)


def store_types_and_artifact_types() -> (
    Generator[Tuple[StoreType, ArtifactType], None, None]
):
    """
    Yield store fixture names and artifact types to produce all combinations.
    :return: (store fixture name, artifact type)
    """
    for store_type in StoreType:
        for artifact_type in ArtifactType:
            yield store_type, artifact_type


@pytest.fixture(scope="function")
def create_test_artifact_store(
    tmpdir_factory,
) -> typing.Callable[[str], ArtifactStore]:
    def _make(store_type) -> ArtifactStore:
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


# The mode identifier for default context
FX_MODEL_ID = "model0"

# The version identifier for default context
FX_VERSION_ID = "v0"


@pytest.fixture(scope="function")
def store_with_context() -> Tuple[ArtifactStore, Context]:
    """Create an in-memory artifact store with initial context."""
    store = create_memory_store()
    with ManagedArtifactSession(store.session()) as artifact_store:
        _ = artifact_store.model_mapper.create(Model(identifier=FX_MODEL_ID))
        _ = artifact_store.version_mapper.create(
            Version(identifier=FX_VERSION_ID),
            FX_MODEL_ID,
        )

    return store, Context(FX_MODEL_ID, FX_VERSION_ID)
