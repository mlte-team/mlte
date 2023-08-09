"""
test/web/store/context/test_version.py

Test the HTTP interface for version operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.context.model import (
    ModelCreate,
    NamespaceCreate,
    Version,
    VersionCreate,
)

from ..fixure.http import clients, mem_client  # noqa


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
    """Versions can be created."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace_and_model("0", "0", client)

    version = VersionCreate(identifier="0")

    res = client.post("/api/namespace/0/model/0/version", json=version.dict())
    assert res.status_code == 200
    _ = Version(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be read."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace_and_model("0", "0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/namespace/0/model/0/version", json=version.dict())
    assert res.status_code == 200

    created = Version(**res.json())

    res = client.get("/api/namespace/0/model/0/version/0")
    assert res.status_code == 200
    read = Version(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be listed."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace_and_model("0", "0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/namespace/0/model/0/version", json=version.dict())
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)
    create_namespace_and_model("0", "0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/namespace/0/model/0/version", json=version.dict())
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete("/api/namespace/0/model/0/version/0")
    assert res.status_code == 200

    res = client.get("/api/namespace/0/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 0


def create_namespace_and_model(
    namespace_id: str, model_id: str, client: TestClient
) -> None:
    """Create a namespace and model with the given identifiers."""
    res = client.post(
        "/api/namespace", json=NamespaceCreate(identifier=namespace_id).dict()
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model",
        json=ModelCreate(identifier=model_id).dict(),
    )
    assert res.status_code == 200
