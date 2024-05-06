"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

from typing import Generator, Tuple

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.context.model import ModelCreate, VersionCreate
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBStore
from test.backend.fixture.http import setup_API_and_test_client
from test.store.artifact import artifact_store_creators

_STORE_FIXTURE_NAMES = ["http_store", "memory_store", "fs_store", "rdbs_store"]


@pytest.fixture(scope="function")
def http_store() -> HttpArtifactStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Set an in memory store and get a test http client, configured for the app.
    client = setup_API_and_test_client()
    return artifact_store_creators.create_http_store(
        username=client.username,
        password=client.password,
        uri=str(client.client.base_url),
        client=client,
    )


@pytest.fixture(scope="function")
def memory_store() -> InMemoryStore:
    """A fixture for an in-memory store."""
    return artifact_store_creators.create_memory_store()


@pytest.fixture(scope="function")
def fs_store(tmp_path) -> LocalFileSystemStore:
    """A fixture for an local FS store."""
    return artifact_store_creators.create_fs_store(tmp_path)


@pytest.fixture(scope="function")
def rdbs_store() -> RelationalDBStore:
    """A fixture for an in-memory RDBS store."""
    return artifact_store_creators.create_rdbs_store()


def artifact_stores() -> Generator[str, None, None]:
    """
    Yield store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        yield store_fixture_name


def artifact_stores_and_types() -> (
    Generator[Tuple[str, ArtifactType, bool], None, None]
):
    """
    Yield store fixture names and artifact types to produce all combinations.
    :return: (store fixture name, artifact type)
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        for type in ArtifactType:
            for complete in [False, True]:
                yield store_fixture_name, type, complete


# The mode identifier for default context
FX_MODEL_ID = "model0"

# The version identifier for default context
FX_VERSION_ID = "v0"


@pytest.fixture(scope="function")
def store_with_context() -> Tuple[ArtifactStore, Context]:
    """Create an in-memory artifact store with initial context."""
    store = artifact_store_creators.create_memory_store()
    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_model(ModelCreate(identifier=FX_MODEL_ID))
        _ = handle.create_version(
            FX_MODEL_ID,
            VersionCreate(identifier=FX_VERSION_ID),
        )

    return store, Context(FX_MODEL_ID, FX_VERSION_ID)
