"""
test/store/test_http.py

Test the HTTP interface for storage server(s).

NOTE: We currently rely on a hack to enable HTTP tests.
Upon import of the fixtures below, the api_router object
is imported. This triggers FastAPI's dependency injection
system to resolve dependencies on routes, namely the
dependency on the backend SessionHandle. Because the fixture-
level data is not available at the time this is evaluated,
the global engine is configured based on the values in the
global settings object. These values are read from the
environment, rather than from the local test configuration.
To avoid engine initialization failures (as a result of
nonexistent resources e.g. directories) we create a single,
temporary directory in test/store/data/store that is used to
initialize the default backend at important time. At test
time, this backend is overridden by the test local config.
"""

from typing import Any, Dict, List, Tuple

import pytest
from deepdiff import DeepDiff
from fastapi.testclient import TestClient

from mlte.store.models import Result, ResultVersion
from .fixture.http import fs_client, fs_handle  # noqa

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
    """Compare results for equality."""
    return not DeepDiff(a, b)


def result_from(
    identifier: str, tag: str, versions: List[Tuple[int, Dict[str, Any]]]
) -> Result:
    """Generate a result with arbitrary data."""
    return Result(
        identifier=identifier,
        tag=tag,
        versions=[ResultVersion(version=e[0], data=e[1]) for e in versions],
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
        "/api/result/m0/v0",
        json=result_from("r0", "", [(0, {"hello": "world"})]).to_json(),
    )
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_read(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that a read on empty store gives expected response."""
    client: TestClient = request.getfixturevalue(client_fixture)

    # Read many results
    res = client.get("/api/result/m0/v0")
    assert res.status_code == 404

    # Read individual result
    res = client.get("/api/result/m0/v0/r0")
    assert res.status_code == 404

    # Read single version
    res = client.get("/api/result/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_delete(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that delete on empty store gives 404."""
    client: TestClient = request.getfixturevalue(client_fixture)

    res = client.delete("/api/result/m0/v0")
    assert res.status_code == 404

    res = client.delete("/api/result/m0/v0/r0")
    assert res.status_code == 404

    res = client.delete("/api/result/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("client_fixture", CLIENTS)
def test_write_read_delete(client_fixture: str, request: pytest.FixtureRequest):
    """Ensure that a written result can be read and deleted."""
    client: TestClient = request.getfixturevalue(client_fixture)

    r = result_from("r0", "", [(0, {"hello": "world"})])

    res = client.post("/api/result/m0/v0", json=r.to_json())
    assert res.status_code == 200

    res = client.get("/api/result/m0/v0/r0")
    assert res.status_code == 200
    assert "results" in res.json()

    results = res.json()["results"]
    assert len(results) == 1
    assert equal(r.versions[0].data, results[0])

    res = client.delete("/api/result/m0/v0/r0")
    assert res.status_code == 200

    res = client.get("/api/result/m0/v0/r0")
    assert res.status_code == 404
