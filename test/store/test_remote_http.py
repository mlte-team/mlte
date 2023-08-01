"""
test/store/test_local_memory.py

Unit tests for the in-memory artifact store implementation.
"""

from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

import mlte.store.error as errors
import mlte.web.store.app_factory as app_factory
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.negotiation.model import NegotiationCardModel
from mlte.store import ManagedSession, StoreURI
from mlte.store.factory import create_store
from mlte.store.underlying.http import (
    ClientType,
    RemoteHttpStore,
    RemoteHttpStoreClient,
)
from mlte.web.store.api.api import api_router
from mlte.web.store.core.config import settings
from mlte.web.store.state import state

# -----------------------------------------------------------------------------
# Client Configuration
# -----------------------------------------------------------------------------


class TestclientCient(RemoteHttpStoreClient):
    def __init__(self, client: TestClient) -> None:
        super().__init__(ClientType.TESTCLIENT)

        self.client = client
        """The underlying client."""

    def get(self, url: str, **kwargs) -> httpx.Response:  # type: ignore[override]
        return self.client.get(url, **kwargs)

    def post(  # type: ignore[override]
        self, url: str, data: Any = None, json: Any = None, **kwargs
    ) -> httpx.Response:
        return self.client.post(url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:  # type: ignore[override]
        return self.client.delete(url, **kwargs)


@pytest.fixture(scope="function")
def store() -> RemoteHttpStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Configure the backing store
    state.set_store(create_store("memory://"))

    # Configure the application
    app = app_factory.create()
    app.include_router(api_router, prefix=settings.API_PREFIX)

    # Return a remote store that is able to hit the app
    client = TestClient(app)
    store = RemoteHttpStore(
        uri=StoreURI.from_string(str(client.base_url)),
        client=TestclientCient(client),
    )
    return store


# -----------------------------------------------------------------------------
# Test Definitions
# -----------------------------------------------------------------------------


def test_init() -> None:
    """A remote HTTP store can be initialized."""
    _ = RemoteHttpStore(StoreURI.from_string("http://localhost:8080"))


def test_fixture(store: RemoteHttpStore) -> None:
    """The fixture for remote HTTP store can be initialized."""
    assert True


def test_namespace(store: RemoteHttpStore) -> None:
    """An in-memory store supports namespace operations."""
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


def test_model(store: RemoteHttpStore) -> None:
    """An in-memory store supports model operations."""
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


def test_version(store: RemoteHttpStore) -> None:
    """An in-memory store supports model version operations."""
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


def test_negotiation_card(store: RemoteHttpStore) -> None:
    """An in-memory store supports negotiation card operations."""

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
        handle.delete_artifact(
            namespace_id, model_id, version_id, card.header.identifier
        )

    with ManagedSession(store.session()) as handle:
        with pytest.raises(errors.ErrorNotFound):
            _ = handle.read_artifact(
                namespace_id, model_id, version_id, card.header.identifier
            )
