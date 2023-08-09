"""
test/web/store/contex/test_model.py

Test the HTTP interface for model operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.context.model import Model, ModelCreate, NamespaceCreate

from ..fixure.http import clients, mem_client  # noqa

# -----------------------------------------------------------------------------
# Tests: Model
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("client_fixture", clients())
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: TestClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be created."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace("0", client)

    model = ModelCreate(identifier="model")

    res = client.post("/api/namespace/0/model", json=model.dict())
    assert res.status_code == 200
    _ = Model(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be read."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace("0", client)

    model = ModelCreate(identifier="0")
    res = client.post("/api/namespace/0/model", json=model.dict())
    assert res.status_code == 200

    created = Model(**res.json())

    res = client.get("/api/namespace/0/model/0")
    assert res.status_code == 200
    read = Model(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespace can be listed."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace("0", client)

    model = ModelCreate(identifier="0")

    res = client.post("/api/namespace/0/model", json=model.dict())
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespaces can be deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace("0", client)

    model = ModelCreate(identifier="0")

    res = client.post("/api/namespace/0/model", json=model.dict())
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model")
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete("/api/namespace/0/model/0")
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model")
    assert res.status_code == 200
    assert len(res.json()) == 0


def create_namespace(id: str, client: TestClient) -> None:
    """Create a namespace with the given identifier."""
    res = client.post(
        "/api/namespace", json=NamespaceCreate(identifier=id).dict()
    )
    assert res.status_code == 200
