"""
test/web/store/artifcat/test_negotiation_card.py

Test the HTTP interface for negotiation card operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.negotiation.model import NegotiationCardModel
from mlte.store.query import Query

from .fixure.http import CLIENTS, mem_client  # noqa


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: TestClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_write(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Negotiation cards can be written."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    artifact = minimal_model("myartifact", ArtifactType.NEGOTIATION_CARD)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=artifact.dict(),
    )
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Negotiation cards can be read."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    artifact = minimal_model("myartifact", ArtifactType.NEGOTIATION_CARD)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=artifact.dict(),
    )
    assert res.status_code == 200

    created = ArtifactModel(**res.json())

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/myartifact"
    )
    assert res.status_code == 200
    read = ArtifactModel(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_search(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Negotiation cards can be searched."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    artifact = minimal_model("myartifact", ArtifactType.NEGOTIATION_CARD)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=artifact.dict(),
    )
    assert res.status_code == 200
    created = ArtifactModel(**res.json())

    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/search",
        json=Query().dict(),
    )
    assert res.status_code == 200

    collection = res.json()
    assert len(collection) == 1

    read = ArtifactModel(**collection[0])
    assert read == created


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Negotiation cards can be deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    artifact = minimal_model("myartifact", ArtifactType.NEGOTIATION_CARD)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=artifact.dict(),
    )
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/myartifact"
    )
    assert res.status_code == 200

    res = client.delete(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/myartifact"
    )
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/myartifact"
    )
    assert res.status_code == 404


def create_context(
    namespace_id: str, model_id: str, version_id: str, client: TestClient
) -> None:
    """Create context for artifacts.."""
    res = client.post(
        "/api/namespace", json=NamespaceCreate(identifier=namespace_id).dict()
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model",
        json=ModelCreate(identifier=model_id).dict(),
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version",
        json=VersionCreate(identifier=version_id).dict(),
    )
    assert res.status_code == 200


def minimal_model(
    artifact_id: str, artifact_type: ArtifactType
) -> ArtifactModel:
    return ArtifactModel(
        header=ArtifactHeaderModel(identifier=artifact_id, type=artifact_type),
        body=minimal_body(artifact_type),
    )


def minimal_body(artifact_type: ArtifactType) -> NegotiationCardModel:
    if artifact_type == ArtifactType.NEGOTIATION_CARD:
        return NegotiationCardModel()
    else:
        assert False, "Unreachable."
