"""
test/store/fixture.py

Fixtures for MLTE artifact store unit tests.
"""

from __future__ import annotations

import typing
from typing import Generator, Optional, Tuple

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.artifact.underlying.http import HttpArtifactStore
from mlte.store.base import StoreType
from mlte.user.model import UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.artifact import artifact_store_creators


def create_api_and_http_store(
    user: Optional[UserWithPassword] = None,
) -> HttpArtifactStore:
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
            return artifact_store_creators.create_memory_store()
        elif store_type == StoreType.LOCAL_FILESYSTEM.value:
            return artifact_store_creators.create_fs_store(
                tmpdir_factory.mktemp("data")
            )
        elif store_type == StoreType.RELATIONAL_DB.value:
            return artifact_store_creators.create_rdbs_store()
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
    store = artifact_store_creators.create_memory_store()
    with ManagedArtifactSession(store.session()) as artifact_store:
        _ = artifact_store.model_mapper.create(Model(identifier=FX_MODEL_ID))
        _ = artifact_store.version_mapper.create(
            Version(identifier=FX_VERSION_ID),
            FX_MODEL_ID,
        )

    return store, Context(FX_MODEL_ID, FX_VERSION_ID)
