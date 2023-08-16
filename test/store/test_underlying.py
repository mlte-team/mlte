"""
test/store/test_underlying.py

Unit tests for the underlying artifact store implementations.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact.model import ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.store import ManagedSession, Store, StoreURI
from mlte.store.underlying.fs import LocalFileSystemStore
from mlte.store.underlying.http import RemoteHttpStore
from mlte.store.underlying.memory import InMemoryStore

from ..fixture.artifact import ArtifactFactory
from .fixture import (  # noqa
    fs_store,
    http_store,
    memory_store,
    stores,
    stores_and_types,
)


def test_init_memory() -> None:
    """An in-memory store can be initialized."""
    _ = InMemoryStore(StoreURI.from_string("memory://"))


def test_init_http() -> None:
    """A remote HTTP store can be initialized."""
    _ = RemoteHttpStore(StoreURI.from_string("http://localhost:8080"))


def test_init_fs(tmp_path) -> None:
    """An local FS store can be initialized."""
    _ = LocalFileSystemStore(StoreURI.from_string(f"local://{tmp_path}"))


@pytest.mark.parametrize("store_fixture_name", stores())
def test_namespace(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports namespace operations."""
    store: Store = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"

    with ManagedSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

    with ManagedSession(store.session()) as handle:
        _ = handle.read_namespace(namespace_id)

    with ManagedSession(store.session()) as handle:
        ids = handle.list_namespaces()
        assert len(ids) == 1

    with ManagedSession(store.session()) as handle:
        _ = handle.delete_namespace(namespace_id)

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_namespace(namespace_id)

    with ManagedSession(store.session()) as handle:
        ids = handle.list_namespaces()
        assert len(ids) == 0


@pytest.mark.parametrize("store_fixture_name", stores())
def test_model(store_fixture_name: str, request: pytest.FixtureRequest) -> None:
    """An artifact store supports model operations."""
    store: Store = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"

    with ManagedSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

    with ManagedSession(store.session()) as handle:
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

    with ManagedSession(store.session()) as handle:
        _ = handle.read_model(namespace_id, model_id)

    with ManagedSession(store.session()) as handle:
        models = handle.list_models(namespace_id)
        assert len(models) == 1

    with ManagedSession(store.session()) as handle:
        handle.delete_model(namespace_id, model_id)

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            handle.read_model(namespace_id, model_id)


@pytest.mark.parametrize("store_fixture_name", stores())
def test_version(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    """An artifact store supports model version operations."""
    store: Store = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

    with ManagedSession(store.session()) as handle:
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    with ManagedSession(store.session()) as handle:
        _ = handle.read_version(namespace_id, model_id, version_id)

    with ManagedSession(store.session()) as handle:
        versions = handle.list_versions(namespace_id, model_id)
        assert len(versions) == 1

    with ManagedSession(store.session()) as handle:
        handle.delete_version(namespace_id, model_id, version_id)

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_version(namespace_id, model_id, version_id)


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_search(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store store supports queries."""
    store: Store = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    a0 = ArtifactFactory.make(artifact_type, "id0")
    a1 = ArtifactFactory.make(artifact_type, "id1")

    with ManagedSession(store.session()) as handle:
        for artifact in [a0, a1]:
            handle.write_artifact(namespace_id, model_id, version_id, artifact)

    with ManagedSession(store.session()) as handle:
        artifacts = handle.search_artifacts(namespace_id, model_id, version_id)
        assert len(artifacts) == 2


@pytest.mark.parametrize("store_fixture_name,artifact_type", stores_and_types())
def test_artifact(
    store_fixture_name: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:
    """An artifact store supports basic artifact operations."""
    store: Store = request.getfixturevalue(store_fixture_name)

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"
    artifact_id = "myid"

    with ManagedSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    artifact = ArtifactFactory.make(artifact_type, artifact_id)

    with ManagedSession(store.session()) as handle:
        handle.write_artifact(namespace_id, model_id, version_id, artifact)

    with ManagedSession(store.session()) as handle:
        _ = handle.read_artifact(
            namespace_id, model_id, version_id, artifact_id
        )

    with ManagedSession(store.session()) as handle:
        read = handle.read_artifacts(namespace_id, model_id, version_id)
        assert len(read) == 1

    with ManagedSession(store.session()) as handle:
        handle.delete_artifact(namespace_id, model_id, version_id, artifact_id)

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_artifact(
                namespace_id, model_id, version_id, artifact_id
            )
