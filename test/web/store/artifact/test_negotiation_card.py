"""
test/web/store/artifcat/test_negotiation_card.py

Test the HTTP interface for negotiation card operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.artifact import ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.negotiation.model import (
    NegotiationCardBodyModel,
    NegotiationCardHeaderModel,
    NegotiationCardModel,
)

from ..fixure.http import CLIENTS, mem_client  # noqa


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

    card = NegotiationCardModel(
        header=NegotiationCardHeaderModel(
            identifier="card", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardBodyModel(),
    )
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card",
        data=card.json(),
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

    card = NegotiationCardModel(
        header=NegotiationCardHeaderModel(
            identifier="card", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardBodyModel(),
    )
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card",
        data=card.json(),
    )
    assert res.status_code == 200

    created = NegotiationCardModel(**res.json())

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card/card"
    )
    assert res.status_code == 200
    read = NegotiationCardModel(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Negotiation cards can be deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    card = NegotiationCardModel(
        header=NegotiationCardHeaderModel(
            identifier="card", type=ArtifactType.NEGOTIATION_CARD
        ),
        body=NegotiationCardBodyModel(),
    )
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card",
        data=card.json(),
    )
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card/card"
    )
    assert res.status_code == 200

    res = client.delete(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card/card"
    )
    print(res.json())
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/negotiation-card/card"
    )
    assert res.status_code == 404


def create_context(
    namespace_id: str, model_id: str, version_id: str, client: TestClient
) -> None:
    """Create context for artifacts.."""
    res = client.post(
        "/api/namespace", data=NamespaceCreate(identifier=namespace_id).json()
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model",
        data=ModelCreate(identifier=model_id).json(),
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version",
        data=VersionCreate(identifier=version_id).json(),
    )
    assert res.status_code == 200
