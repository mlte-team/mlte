"""
test/store/test_namespace.py

Test the HTTP interface for namespace operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.context.model import Namespace, NamespaceCreate

from .fixure.http import CLIENTS, mem_client  # noqa

# -----------------------------------------------------------------------------
# Tests: Namespace
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: TestClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespace can be created."""
    client: TestClient = request.getfixturevalue(client_fixture)

    ns = NamespaceCreate(identifier="id")

    res = client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200
    _ = Namespace(**res.json())


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespace can be read."""
    client: TestClient = request.getfixturevalue(client_fixture)

    ns = NamespaceCreate(identifier="id")

    res = client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200
    created = Namespace(**res.json())

    res = client.get("/api/namespace/id")
    assert res.status_code == 200
    read = Namespace(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespace can be listed."""
    client: TestClient = request.getfixturevalue(client_fixture)

    ns = NamespaceCreate(identifier="id")

    res = client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200

    res = client.get("/api/namespace")
    assert res.status_code == 200
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Namespaces can be deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)

    ns = NamespaceCreate(identifier="id")

    res = client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200

    res = client.get("/api/namespace")
    assert res.status_code == 200
    assert len(res.json()) == 1

    res = client.delete("/api/namespace/id")
    assert res.status_code == 200

    res = client.get("/api/namespace")
    assert res.status_code == 200
    assert len(res.json()) == 0
