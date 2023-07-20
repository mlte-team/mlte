"""
test/store/test_local_memory.py

Unit tests for the in-memory artifact store implementation.
"""

import pytest

import mlte.store.error as errors
from mlte.context.model import Model, Namespace, Version
from mlte.store import StoreURI
from mlte.store.underlying.memory import InMemoryStore, InMemoryStoreSession


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
        handle: InMemoryStoreSession = handle
        handle.create_namespace(Namespace(identifier=namespace_id))

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        _ = handle.read_namespace(namespace_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.delete_namespace(namespace_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_namespace(namespace_id)


def test_model(store: InMemoryStore) -> None:
    """An in-memory store supports model operations."""
    namespace_id = "namespace"
    model_id = "model"

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.create_namespace(Namespace(identifier=namespace_id))

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.create_model(namespace_id, Model(identifier=model_id))

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        _ = handle.read_model(namespace_id, model_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.delete_model(namespace_id, model_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        with pytest.raises(errors.ErrorNotFound):
            handle.read_model(namespace_id, model_id)


def test_version(store: InMemoryStore) -> None:
    """An in-memory store supports model version operations."""
    namespace_id = "namespace"
    model_id = "model"
    version_id = "version"

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.create_namespace(Namespace(identifier=namespace_id))
        handle.create_model(namespace_id, Model(identifier=model_id))

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.create_version(
            namespace_id, model_id, Version(identifier=version_id)
        )

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        _ = handle.read_version(namespace_id, model_id, version_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        handle.delete_version(namespace_id, model_id, version_id)

    with store.session() as handle:
        handle: InMemoryStoreSession = handle
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_version(namespace_id, model_id, version_id)
