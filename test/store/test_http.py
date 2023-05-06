"""
test/store/test_http.py

Test the HTTP interface for storage server(s).
"""

from typing import Any, Dict, List, Tuple

import pytest
from deepdiff import DeepDiff
from fastapi.testclient import TestClient

from mlte.store.models import Value, ValueVersion
from .fixture.http import fs_client, fs_engine  # noqa

# -----------------------------------------------------------------------------
# Test Definitions
# -----------------------------------------------------------------------------

"""
This list contains the global collection of test clients.
However, because we cannot directly parametrize a test with
a fixture function, we specify via strings and then use the
`request` fixture to translate this into the actual fixture.
"""
CLIENTS = ["fs_client"]

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """Compare values for equality."""
    return not DeepDiff(a, b)


def value_from(
    identifier: str, tag: str, versions: List[Tuple[int, Dict[str, Any]]]
) -> Value:
    """Generate a value with arbitrary data."""
    return Value(
        identifier=identifier,
        tag=tag,
        versions=[ValueVersion(version=e[0], data=e[1]) for e in versions],
    )


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_init(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that server can initialize."""
    client: TestClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_write(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that write can be performed successfully."""
    client: TestClient = request.getfixturevalue(client_fixture)

    res = client.post(
        "/api/value/m0/v0",
        json=value_from("r0", "", [(0, {"hello": "world"})]).to_json(),
    )
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_read(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that a read on empty store gives expected response."""
    client: TestClient = request.getfixturevalue(client_fixture)

    # Read many values
    res = client.get("/api/value/m0/v0")
    assert res.status_code == 404

    # Read individual value
    res = client.get("/api/value/m0/v0/r0")
    assert res.status_code == 404

    # Read single version
    res = client.get("/api/value/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_delete(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that delete on empty store gives 404."""
    client: TestClient = request.getfixturevalue(client_fixture)

    res = client.delete("/api/value/m0/v0")
    assert res.status_code == 404

    res = client.delete("/api/value/m0/v0/r0")
    assert res.status_code == 404

    res = client.delete("/api/value/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_write_read_delete(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that a written value can be read and deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)

    r = value_from("r0", "", [(0, {"hello": "world"})])

    res = client.post("/api/value/m0/v0", json=r.to_json())
    assert res.status_code == 200

    res = client.get("/api/value/m0/v0/r0")
    assert res.status_code == 200
    assert "values" in res.json()

    values = res.json()["values"]
    assert len(values) == 1
    assert equal(r.versions[0].data, values[0])

    res = client.delete("/api/value/m0/v0/r0")
    assert res.status_code == 200

    res = client.get("/api/value/m0/v0/r0")
    assert res.status_code == 404
