"""
test/store/test_underlying.py

Unit tests for the underlying artifact store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import (
    ArtifactStoreSession,
    ManagedArtifactSession,
)
from mlte.store.query import Query, TypeFilter
from test.backend.fixture.user_generator import TEST_API_USERNAME
from test.store.artifact import artifact_store_creators

from ...fixture.artifact import ArtifactModelFactory
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
        handle.model_mapper.create(Model(identifier=model_id))

        _ = handle.model_mapper.read(model_id)

        models = handle.model_mapper.list()
        assert len(models) == 1

        handle.model_mapper.delete(model_id)

        with pytest.raises(errors.ErrorNotFound):
            handle.model_mapper.read(model_id)


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_model_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Models can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.model_mapper.create(Model(identifier=model_id))

        models = handle.model_mapper.list()
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
        handle.model_mapper.create(Model(identifier=model_id))

        handle.version_mapper.create(Version(identifier=version_id), model_id)

        _ = handle.version_mapper.read(version_id, model_id)

        versions = handle.version_mapper.list(model_id)
        assert len(versions) == 1

        handle.version_mapper.delete(model_id, version_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.version_mapper.read(version_id, model_id)


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_two_versions_same_id_same_model(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store does't allow creating two versions with same id if they are in the same model."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        with pytest.raises(errors.ErrorAlreadyExists):
            handle.version_mapper.create(
                Version(identifier=version_id), model_id
            )


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
        handle.model_mapper.create(Model(identifier=model_id))
        handle.model_mapper.create(Model(identifier=model2_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        # No assert needed, just ensure that this doesn't throw an exception.
        handle.version_mapper.create(Version(identifier=version_id), model2_id)


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_version_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Versions can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        versions = handle.version_mapper.list(model_id)
        assert len(versions) == 1
        assert versions[0] == "version0"


def check_artifact_writing(
    handle: ArtifactStoreSession,
    model_id: str,
    version_id: str,
    artifact_id: str,
    artifact: ArtifactModel,
    user: str,
) -> ArtifactModel:
    """Helper function that writes an artifact, and then reads it and check they are the same."""
    # First write it.
    artifact = handle.artifact_mapper._add_header_data(artifact, user)
    written_artifact = handle.artifact_mapper.write_artifact(
        model_id, version_id, artifact
    )
    artifact.header.identifier = written_artifact.header.identifier
    artifact_id = artifact.header.identifier

    # Then read it from storage.
    read = handle.artifact_mapper.read(artifact_id, (model_id, version_id))

    # Ignore creator and timestamp changes.
    read.header.timestamp = artifact.header.timestamp
    read.header.creator = artifact.header.creator

    # Check that we have the same artifact.
    assert artifact.to_json() == read.to_json()

    return written_artifact


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type", artifact_stores_and_types()
)
def test_search(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store store supports queries."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        a0 = ArtifactModelFactory.make(artifact_type, "id0")
        a1 = ArtifactModelFactory.make(artifact_type, "id1")

        for artifact in [a0, a1]:
            handle.artifact_mapper.write_artifact(
                model_id, version_id, artifact
            )

        artifacts = handle.artifact_mapper.search(
            Query(filter=TypeFilter(item_type=artifact_type)),
            (model_id, version_id),
        )
        assert len(artifacts) == 2


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type", artifact_stores_and_types()
)
def test_artifact(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store supports basic artifact operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"
    user = TEST_API_USERNAME

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        artifact = ArtifactModelFactory.make(artifact_type, artifact_id)
        artifact_id = artifact.header.identifier

        # First check we can write and load an artifact.
        written_artifact = check_artifact_writing(
            handle, model_id, version_id, artifact_id, artifact, user
        )
        artifact_id = written_artifact.header.identifier

        # Second check that we can delete the artifact, and that it is really deleted.
        handle.artifact_mapper.delete(artifact_id, (model_id, version_id))

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.artifact_mapper.read(artifact_id, (model_id, version_id))

        # Third, try writing the artifact again, to ensure we can re-write an artifact after it was deleted, and there are no weird leftovers.
        check_artifact_writing(
            handle, model_id, version_id, artifact_id, artifact, user
        )


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type", artifact_stores_and_types()
)
def test_artifact_without_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact does not create organizational elements by default, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    artifact = ArtifactModelFactory.make(artifact_type, artifact_id)
    artifact_id = artifact.header.identifier

    # The write fails
    with pytest.raises(errors.ErrorNotFound):
        with ManagedArtifactSession(store.session()) as handle:
            handle.artifact_mapper.write_artifact(
                model_id, version_id, artifact
            )


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type", artifact_stores_and_types()
)
def test_artifact_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store can create organizational elements implicitly, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    artifact = ArtifactModelFactory.make(artifact_type, artifact_id)
    artifact_id = artifact.header.identifier

    # The write succeeds
    with ManagedArtifactSession(store.session()) as handle:
        written_artifact = handle.artifact_mapper.write_artifact(
            model_id, version_id, artifact
        )
        artifact_id = written_artifact.header.identifier

        # The organizational elements are present
        assert len(handle.model_mapper.list()) == 1
        assert len(handle.version_mapper.list(model_id)) == 1

        # The artifact is present
        handle.artifact_mapper.read(artifact_id, (model_id, version_id))


@pytest.mark.parametrize(
    "store_fixture_name,artifact_type", artifact_stores_and_types()
)
def test_artifact_overwrite(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact cam be overwritten with the `force` option."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model0"
    version_id = "version0"
    artifact_id = "myid"

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)

        artifact = ArtifactModelFactory.make(artifact_type, artifact_id)

        # The initial write succeeds
        written_artifact = handle.artifact_mapper.write_artifact(
            model_id, version_id, artifact
        )
        artifact_id = written_artifact.header.identifier

        # Another attempt to write fails
        with pytest.raises(errors.ErrorAlreadyExists):
            handle.artifact_mapper.write_artifact(
                model_id,
                version_id,
                artifact,
            )

        # Attempt to write with `force` succeeds
        handle.artifact_mapper.write_artifact(
            model_id, version_id, artifact, force=True
        )


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_invalid_chars(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Test creation with chars that may be invalid in some storage types."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    model_id = "model/test"
    version_id = "version/test"
    artifact_id = "myid/test"
    user = TEST_API_USERNAME

    with ManagedArtifactSession(store.session()) as handle:
        handle.model_mapper.create(Model(identifier=model_id))
        handle.version_mapper.create(Version(identifier=version_id), model_id)
        artifact = ArtifactModelFactory.make(ArtifactType.REPORT, artifact_id)
        handle.artifact_mapper.write_artifact_with_header(
            model_id, version_id, artifact, user=user
        )
