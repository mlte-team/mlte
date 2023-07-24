"""
test/store/test_local_memory.py

Unit tests for the in-memory artifact store implementation.
"""

import pytest

import mlte.store.error as errors
from mlte.artifact import ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.negotiation.model import (
    NegotiationCardBodyModel,
    NegotiationCardHeaderModel,
    NegotiationCardModel,
)
from mlte.store import StoreURI
from mlte.store.underlying.memory import InMemoryStore


@pytest.fixture(scope="function")
def store() -> InMemoryStore:
    """A fixture for an in-memory store."""
    return InMemoryStore(StoreURI.from_string("memory://"))


def test_init() -> None:
    """An in-memory store can be initialized."""
    _ = InMemoryStore(StoreURI.from_string("memory://"))


def test_namespace(store: InMemoryStore) -> None:
    """An in-memory store supports namespace operations."""
    namespace_id = "namespace"

    with store.session() as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

    with store.session() as handle:
        _ = handle.read_namespace(namespace_id)

    with store.session() as handle:
        ids = handle.list_namespaces()
        assert len(ids) == 1

    with store.session() as handle:
        _ = handle.delete_namespace(namespace_id)

    with store.session() as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_namespace(namespace_id)

    with store.session() as handle:
        ids = handle.list_namespaces()
        assert len(ids) == 0


def test_model(store: InMemoryStore) -> None:
    """An in-memory store supports model operations."""
    namespace_id = "namespace"
    model_id = "model"

    with store.session() as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=namespace_id))

    with store.session() as handle:
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

    with store.session() as handle:
        _ = handle.read_model(namespace_id, model_id)

    with store.session() as handle:
        handle.delete_model(namespace_id, model_id)

    with store.session() as handle:
        with pytest.raises(errors.ErrorNotFound):
            handle.read_model(namespace_id, model_id)


def test_version(store: InMemoryStore) -> None:
    """An in-memory store supports model version operations."""
    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with store.session() as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))

    with store.session() as handle:
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    with store.session() as handle:
        _ = handle.read_version(namespace_id, model_id, version_id)

    with store.session() as handle:
        handle.delete_version(namespace_id, model_id, version_id)

    with store.session() as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_version(namespace_id, model_id, version_id)


def test_negotiation_card(store: InMemoryStore) -> None:
    """An in-memory store supports negotiation card operations."""

    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with store.session() as handle:
        handle.create_namespace(NamespaceCreate(identifier=namespace_id))
        handle.create_model(namespace_id, ModelCreate(identifier=model_id))
        handle.create_version(
            namespace_id, model_id, VersionCreate(identifier=version_id)
        )

    card = NegotiationCardModel(
        header=NegotiationCardHeaderModel(
            identifier="id", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardBodyModel(),
    )

    with store.session() as handle:
        handle.create_negotiation_card(namespace_id, model_id, version_id, card)

    with store.session() as handle:
        _ = handle.read_negotiation_card(
            namespace_id, model_id, version_id, card.header.identifier
        )

    with store.session() as handle:
        handle.delete_negotiation_card(
            namespace_id, model_id, version_id, card.header.identifier
        )

    with store.session() as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_negotiation_card(
                namespace_id, model_id, version_id, card.header.identifier
            )
