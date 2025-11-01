"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

from typing import Generator, Optional, Tuple

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.artifact.underlying.fs import LocalFileSystemStore
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.artifact.underlying.memory import InMemoryStore
from mlte.store.artifact.underlying.rdbs.store import RelationalDBArtifactStore
from mlte.user.model import UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.artifact import artifact_store_creators

_STORE_FIXTURE_NAMES = ["http_store", "memory_store", "fs_store", "rdbs_store"]


@pytest.fixture(scope="function")
def http_store(user: Optional[UserWithPassword] = None) -> HttpArtifactStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Set an in memory store and get a test http client, configured for the app.
    if user is None:
        user = user_generator.build_admin_user()
    test_api = TestAPI(user=user)
    client = test_api.get_test_client()

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
def rdbs_store() -> RelationalDBArtifactStore:
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
    Generator[Tuple[str, ArtifactType], None, None]
):
    """
    Yield store fixture names and artifact types to produce all combinations.
    :return: (store fixture name, artifact type)
    """
    for store_fixture_name in _STORE_FIXTURE_NAMES:
        for type in ArtifactType:
            yield store_fixture_name, type


# The mode identifier for default context
FX_MODEL_ID = "model0"

# The version identifier for default context
FX_VERSION_ID = "v0"


@pytest.fixture(scope="function")
def store_with_context() -> Tuple[ArtifactStore, Context]:
    """Create an in-memory artifact store with initial context."""
    store = artifact_store_creators.create_memory_store()
    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.model_mapper.create(Model(identifier=FX_MODEL_ID))
        _ = handle.version_mapper.create(
            Version(identifier=FX_VERSION_ID),
            FX_MODEL_ID,
        )

    return store, Context(FX_MODEL_ID, FX_VERSION_ID)
