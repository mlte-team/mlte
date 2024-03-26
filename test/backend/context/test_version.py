"""
test/backend/context/test_version.py

Test the HTTP interface for version operations.
"""

import pytest

from mlte.context.model import ModelCreate, Version, VersionCreate

from ..fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)


@pytest.mark.parametrize("client_fixture", clients())
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    create_model("0", client)

    version = VersionCreate(identifier="0")

    res = client.post("/api/model/0/version", json=version.model_dump())
    assert res.status_code == 200
    _ = Version(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    create_model("0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/model/0/version", json=version.model_dump())
    assert res.status_code == 200

    created = Version(**res.json())

    res = client.get("/api/model/0/version/0")
    assert res.status_code == 200
    read = Version(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    create_model("0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/model/0/version", json=version.model_dump())
    assert res.status_code == 200

    res = client.get("/api/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    create_model("0", client)

    version = VersionCreate(identifier="0")
    res = client.post("/api/model/0/version", json=version.model_dump())
    assert res.status_code == 200

    res = client.get("/api/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete("/api/model/0/version/0")
    assert res.status_code == 200

    res = client.get("/api/model/0/version")
    assert res.status_code == 200
    assert len(res.json()) == 0


def create_model(model_id: str, client: FastAPITestHttpClient) -> None:
    """Create a model with the given identifier."""
    res = client.post(
        "/api/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == 200
