"""
test/store/test_underlying.py

Unit tests for the underlying artifact store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact.type import ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.artifact.underlying.http import RemoteHttpStore
from mlte.store.base import StoreURI

from ...fixture.artifact import ArtifactFactory
from .fixture import (  # noqa
    create_fs_store,
    create_memory_store,
    create_rdbs_store,
    fs_store,
    http_store,
    memory_store,
    rdbs_store,
    stores,
    stores_and_types,
)


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = create_memory_store()


def test_init_http() -> None:
    """A remote HTTP store can be initialized."""
    _ = RemoteHttpStore(StoreURI.from_string("http://localhost:8080"))


def test_init_fs(tmp_path) -> None:
    """An local FS store can be initialized."""
    _ = create_fs_store(tmp_path)


def test_init_rdbs() -> None:
    """A relational DB store can be initialized."""
    _ = create_rdbs_store()


@pytest.mark.parametrize("store_fixture_name", stores())
def test_namespace(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports namespace operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "ns0"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

        _ = handle.read_namespace(namespace_id)

        ids = handle.list_namespaces()
        assert len(ids) == 1

        _ = handle.delete_namespace(namespace_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_namespace(namespace_id)

        ids = handle.list_namespaces()
        assert len(ids) == 0


@pytest.mark.parametrize("store_fixture_name", stores())
def test_namespace_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Namespaces can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "ns0"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

        namespaces = handle.list_namespaces()
        assert len(namespaces) == 1
        assert namespaces[0] == "ns0"


@pytest.mark.parametrize("store_fixture_name", stores())
def test_model(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports model operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

        _ = handle.read_model(namespace_id, model_id)

        models = handle.list_models(namespace_id)
        assert len(models) == 1

        handle.delete_model(namespace_id, model_id)

        with pytest.raises(errors.ErrorNotFound):
            handle.read_model(namespace_id, model_id)


@pytest.mark.parametrize("store_fixture_name", stores())
def test_model_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Models can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "ns0"
    model_id = "model0"

    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        _ = handle.create_model(namespace_id, ModelCreate(identifier=model_id))

        models = handle.list_models(namespace_id)
        assert len(models) == 1
        assert models[0] == "model0"


@pytest.mark.parametrize("store_fixture_name", stores())
def test_version(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports model version operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

        _ = handle.read_version(namespace_id, model_id, version_id)

        versions = handle.list_versions(namespace_id, model_id)
        assert len(versions) == 1

        handle.delete_version(namespace_id, model_id, version_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_version(namespace_id, model_id, version_id)


@pytest.mark.parametrize("store_fixture_name", stores())
def test_version_list(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """Versions can be listed."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "ns0"
    model_id = "model0"
    version_id = "version0"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

        versions = handle.list_versions(namespace_id, model_id)
        assert len(versions) == 1
        assert versions[0] == "version0"


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_search(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store store supports queries."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

        a0 = ArtifactFactory.make(artifact_type, "id0")
        a1 = ArtifactFactory.make(artifact_type, "id1")

        for artifact in [a0, a1]:
            handle.write_artifact(namespace_id, model_id, version_id, artifact)

        artifacts = handle.search_artifacts(namespace_id, model_id, version_id)
        assert len(artifacts) == 2


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_artifact(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store supports basic artifact operations."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"
    artifact_id = "myid"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

        artifact = ArtifactFactory.make(artifact_type, artifact_id)

        handle.write_artifact(namespace_id, model_id, version_id, artifact)

        _ = handle.read_artifact(
            namespace_id, model_id, version_id, artifact_id
        )

        read = handle.read_artifacts(namespace_id, model_id, version_id)
        assert len(read) == 1

        handle.delete_artifact(namespace_id, model_id, version_id, artifact_id)

        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_artifact(
                namespace_id, model_id, version_id, artifact_id
            )


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_artifact_without_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact does not create organizational elements by default, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"
    artifact_id = "myid"

    artifact = ArtifactFactory.make(artifact_type, artifact_id)

    # The write fails
    with pytest.raises(errors.ErrorNotFound):
        with ManagedArtifactSession(store.session()) as handle:
            _ = handle.write_artifact(
                namespace_id, model_id, version_id, artifact
            )


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_artifact_parents(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store can create organizational elements implicitly, on write."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"
    artifact_id = "myid"

    artifact = ArtifactFactory.make(artifact_type, artifact_id)

    # The write succeeds
    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.write_artifact(
            namespace_id, model_id, version_id, artifact, parents=True
        )

        # The organizational elements are present
        assert len(handle.list_namespaces()) == 1
        assert len(handle.list_models(namespace_id)) == 1
        assert len(handle.list_versions(namespace_id, model_id)) == 1

        # The artifact is present
        read = handle.read_artifacts(namespace_id, model_id, version_id)
        assert len(read) == 1


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_artifact_overwrite(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact cam be overwritten with the `force` option."""
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"
    artifact_id = "myid"

    with ManagedArtifactSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

        artifact = ArtifactFactory.make(artifact_type, artifact_id)

        # The initial write succeeds
        _ = handle.write_artifact(
            namespace_id,
            model_id,
            version_id,
            artifact,
        )

        # Another attempt to write fails
        with pytest.raises(errors.ErrorAlreadyExists):
            _ = handle.write_artifact(
                namespace_id,
                model_id,
                version_id,
                artifact,
            )

        # Attempt to write with `force` succeeds
        _ = handle.write_artifact(
            namespace_id, model_id, version_id, artifact, force=True
        )
