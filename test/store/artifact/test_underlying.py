"""
test/store/test_underlying.py

Unit tests for the underlying artifact store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.store.artifact.store import (
    ArtifactStore,
    ArtifactStoreSession,
    ManagedArtifactSession,
)
from test.backend.fixture.user_generator import TEST_API_USERNAME
from test.store.artifact import artifact_store_creators

from ...fixture.artifact import ArtifactFactory
from .fixture import (  # noqa
    artifact_stores,
    artifact_stores_and_types,
    fs_store,
    http_store,
    memory_store,
    rdbs_store,
)


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = artifact_store_creators.create_memory_store()


def test_init_http() -> None:
    """A remote HTTP store can be initialized."""
    _ = artifact_store_creators.create_http_store()


def test_init_fs(tmp_path) -> None:
    """An local FS store can be initialized."""
    _ = artifact_store_creators.create_fs_store(tmp_path)


def test_init_rdbs() -> None:
    """A relational DB store can be initialized."""
    _ = artifact_store_creators.create_rdbs_store()


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_model(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports model operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))

        _ = handle.read_model(model_id)

        models = handle.list_models()
        assert len(models) == 1

        handle.delete_model(model_id)

        with pytest.raises(errors.ErrorNotFound):
            handle.read_model(model_id)


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_model_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Models can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_model(Model(identifier=model_id))

        models = handle.list_models()
        assert len(models) == 1
        assert models[0] == "model0"


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_version(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports model version operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))

        handle.create_version(model_id, Version(identifier=version_id))

        _ = handle.read_version(model_id, version_id)

        versions = handle.list_versions(model_id)
        assert len(versions) == 1

        handle.delete_version(model_id, version_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_version(model_id, version_id)


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_two_versions_same_id_same_model(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store does't allow creating two versions with same id if they are in the same model."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_version(model_id, Version(identifier=version_id))

        with pytest.raises(errors.ErrorAlreadyExists):
            handle.create_version(model_id, Version(identifier=version_id))


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_two_versions_same_id_different_model(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store can create two versions with same id if they are in different models."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model1"
    model2_id = "model2"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_model(Model(identifier=model2_id))
        handle.create_version(model_id, Version(identifier=version_id))

        # No assert needed, just ensure that this doesn't throw an exception.
        handle.create_version(model2_id, Version(identifier=version_id))


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_version_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Versions can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_version(model_id, Version(identifier=version_id))

        versions = handle.list_versions(model_id)
        assert len(versions) == 1
        assert versions[0] == "version0"


def check_artifact_writing(
    handle: ArtifactStoreSession,
    model_id: str,
    version_id: str,
    artifact_id: str,
    artifact: ArtifactModel,
    user: str,
):
    """Helper function that writes an artifact, and then reads it and check they are the same."""
    # First write it.
    handle.write_artifact_with_header(model_id, version_id, artifact, user=user)

    # Then read it from storage.
    read = handle.read_artifact(model_id, version_id, artifact_id)

    # Ignore creator and timestamp changes.
    read.header.timestamp = artifact.header.timestamp
    read.header.creator = artifact.header.creator

    # Check that we have the same artifact.
    assert artifact.to_json() == read.to_json()


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type,complete", artifact_stores_and_types()
)
def test_search(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    complete: bool,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store store supports queries."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_version(model_id, Version(identifier=version_id))

        a0 = ArtifactFactory.make(artifact_type, "id0", complete=complete)
        a1 = ArtifactFactory.make(artifact_type, "id1", complete=complete)

        for artifact in [a0, a1]:
            handle.write_artifact(model_id, version_id, artifact)

        artifacts = handle.search_artifacts(model_id, version_id)
        assert len(artifacts) == 2


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type,complete", artifact_stores_and_types()
)
def test_artifact(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    complete: bool,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store supports basic artifact operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"
    user = TEST_API_USERNAME

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_version(model_id, Version(identifier=version_id))

        artifact = ArtifactFactory.make(
            artifact_type, artifact_id, complete=complete
        )

        # First check we can write and load an artifact.
        check_artifact_writing(
            handle, model_id, version_id, artifact_id, artifact, user
        )

        # Second check that we can delete the artifact, and that it is really deleted.
        handle.delete_artifact(model_id, version_id, artifact_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_artifact(model_id, version_id, artifact_id)

        # Third, try writing the artifact again, to ensure we can re-write an artifact after it was deleted, and there are no weird leftovers.
        check_artifact_writing(
            handle, model_id, version_id, artifact_id, artifact, user
        )


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type,complete", artifact_stores_and_types()
)
def test_artifact_without_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    complete: bool,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact does not create organizational elements by default, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    artifact = ArtifactFactory.make(
        artifact_type, artifact_id, complete=complete
    )

    # The write fails
    with pytest.raises(errors.ErrorNotFound):
        with ManagedArtifactSession(store.session()) as handle:
            _ = handle.write_artifact(model_id, version_id, artifact)


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type,complete", artifact_stores_and_types()
)
def test_artifact_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    complete: bool,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store can create organizational elements implicitly, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    artifact = ArtifactFactory.make(
        artifact_type, artifact_id, complete=complete
    )

    # The write succeeds
    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.write_artifact(model_id, version_id, artifact, parents=True)

        # The organizational elements are present
        assert len(handle.list_models()) == 1
        assert len(handle.list_versions(model_id)) == 1

        # The artifact is present
        read = handle.read_artifacts(model_id, version_id)
        assert len(read) == 1


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type,complete", artifact_stores_and_types()
)
def test_artifact_overwrite(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    complete: bool,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact cam be overwritten with the `force` option."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_model(Model(identifier=model_id))
        handle.create_version(model_id, Version(identifier=version_id))

        artifact = ArtifactFactory.make(
            artifact_type, artifact_id, complete=complete
        )

        # The initial write succeeds
        _ = handle.write_artifact(
            model_id,
            version_id,
            artifact,
        )

        # Another attempt to write fails
        with pytest.raises(errors.ErrorAlreadyExists):
            _ = handle.write_artifact(
                model_id,
                version_id,
                artifact,
            )

        # Attempt to write with `force` succeeds
        _ = handle.write_artifact(model_id, version_id, artifact, force=True)
