"""
test/store/test_http.py

Test the HTTP interface for storage server(s).
"""

from typing import Any, Dict

from deepdiff import DeepDiff
from fastapi.testclient import TestClient

from mlte.context.model import Namespace

from .fixure.http import mem_client  # noqa

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_init(mem_client: TestClient):
    """The server can initialize."""
    res = mem_client.get("/api/healthz")
    assert res.status_code == 200


def test_namespace(mem_client: TestClient) -> None:
    """Namespaces can be created, read, and deleted."""
    ns = Namespace(identifier="id")

    res = mem_client.post("/api/namespace", data=ns.json())
    assert res.status_code == 200

    res = mem_client.get("/api/namespace")
    assert len(res.json()) == 1

    res = mem_client.get("/api/namespace/id")
    deserialized = Namespace.from_json(res.json())
    assert deserialized == ns


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """Compare values for equality."""
    return not DeepDiff(a, b)
