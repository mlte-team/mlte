"""
test/store/test_local_fs.py

Unit tests for the local File System artifact store implementation.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.negotiation.model import NegotiationCardModel
from mlte.store import ManagedSession, StoreURI
from mlte.store.underlying.fs import LocalFileSystemStore


@pytest.fixture(scope="function")
def store(tmp_path) -> LocalFileSystemStore:
    """A fixture for an local FS store."""
    return LocalFileSystemStore(StoreURI.from_string(f"local://{tmp_path}"))


def test_init(tmp_path) -> None:
    """An local FS store can be initialized."""
    _ = LocalFileSystemStore(StoreURI.from_string(f"local://{tmp_path}"))


def test_namespace(store: LocalFileSystemStore) -> None:
    """An local FS store supports namespace operations."""
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


def test_model(store: LocalFileSystemStore) -> None:
    """An local FS store supports model operations."""
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


def test_version(store: LocalFileSystemStore) -> None:
    """An local FS store supports model version operations."""
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


def test_search(store: LocalFileSystemStore) -> None:
    """An local FS store supports queries."""

    # TODO(Kyle): Make this parametric over artifact types.

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    card0 = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id0", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )

    card1 = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id1", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )

    with ManagedSession(store.session()) as handle:
        for artifact in [card0, card1]:
            handle.write_artifact(namespace_id, model_id, version_id, artifact)

    with ManagedSession(store.session()) as handle:
        artifacts = handle.search_artifacts(namespace_id, model_id, version_id)
        assert len(artifacts) == 2


def test_negotiation_card(store: LocalFileSystemStore) -> None:
    """An local FS store supports negotiation card operations."""

    # TODO(Kyle): Make this parametric over artifact types.

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with ManagedSession(store.session()) as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    card = ArtifactModel(
        header=ArtifactHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardModel(),
    )

    with ManagedSession(store.session()) as handle:
        handle.write_artifact(namespace_id, model_id, version_id, card)

    with ManagedSession(store.session()) as handle:
        _ = handle.read_artifact(
            namespace_id, model_id, version_id, card.header.identifier
        )

    with ManagedSession(store.session()) as handle:
        read = handle.read_artifacts(namespace_id, model_id, version_id)
        assert len(read) == 1

    with ManagedSession(store.session()) as handle:
        handle.delete_artifact(
            namespace_id, model_id, version_id, card.header.identifier
        )

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_artifact(
                namespace_id, model_id, version_id, card.header.identifier
            )
