"""
test/store/test_http.py

Test the HTTP interface for storage server(s).
"""

from fastapi.testclient import TestClient

from mlte.context.model import Namespace, NamespaceCreate

from .fixure.http import mem_client  # noqa

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_init(mem_client: TestClient):  # noqa
    """The server can initialize."""
    res = mem_client.get("/api/healthz")
    assert res.status_code == 200


def test_namespace_create(mem_client: TestClient) -> None:  # noqa
    """Namespace can be created."""
    ns = NamespaceCreate(identifier="id")

    res = mem_client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200
    _ = Namespace(**res.json())


def test_namespace_read(mem_client: TestClient) -> None:  # noqa
    """Namespace can be read."""
    ns = NamespaceCreate(identifier="id")

    res = mem_client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200
    created = Namespace(**res.json())

    res = mem_client.get("/api/namespace/id")
    assert res.status_code == 200
    read = Namespace(**res.json())
    assert read == created


def test_namespace_list(mem_client: TestClient) -> None:  # noqa
    """Namespace can be listed."""
    ns = NamespaceCreate(identifier="id")

    res = mem_client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200

    res = mem_client.get("/api/namespace")
    assert res.status_code == 200
    assert len(res.json()) == 1
