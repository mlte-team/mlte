"""
Test the HTTP interface for storage server(s).
"""

from copy import deepcopy
from typing import Any, Dict, List, Tuple

import pytest
from deepdiff import DeepDiff

from mlte.store.frontend.models import Result, ResultVersion
from .support.http import TestDefinition, delete, get, post
from .support.http.fs import (
    create_store_uri,
    create_temporary_directory,
    delete_temporary_directory,
)

# -----------------------------------------------------------------------------
# Test Definitions
# -----------------------------------------------------------------------------

"""
This list contains the global collection of test definitions that
are executed for each test. Adding a new backend consists of
adding a new TestDefinition to this collection as appropriate.
"""
DEFINITIONS = [
    TestDefinition(
        "fs",
        ["--backend-store-uri", "artifact:uri"],
        {},
        [create_temporary_directory, create_store_uri],
        [delete_temporary_directory],
    )
]

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


@pytest.fixture()
def server(request):
    """A fixture to perform setup and teardown."""
    d: TestDefinition = request.param
    try:
        d.setup()
        yield d
    finally:
        d.teardown()


def equal(a: Result, b: Result) -> bool:
    """Compare results for equality."""
    return not DeepDiff(a.to_json(), b.to_json())


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


@pytest.mark.parametrize("server", deepcopy(DEFINITIONS), indirect=["server"])
def test_init(server):
    """Ensure that server can initialize."""
    d: TestDefinition = server
    d.start()

    res = get("/healthcheck")
    assert res.status_code == 200


@pytest.mark.parametrize("server", deepcopy(DEFINITIONS), indirect=["server"])
def test_write(server):
    """Ensure that write can be performed successfully."""
    d: TestDefinition = server
    d.start()

    res = post(
        "/result/m0/v0",
        json=result_from("r0", "", [(0, {"hello": "world"})]).to_json(),
    )
    assert res.status_code == 200


@pytest.mark.parametrize("server", deepcopy(DEFINITIONS), indirect=["server"])
def test_read(server):
    """Ensure that a read on empty store gives 404."""
    d: TestDefinition = server
    d.start()

    # Read many results
    res = get("/result/m0/v0")
    assert res.status_code == 404

    # Read individual result
    res = get("/result/m0/v0/r0")
    assert res.status_code == 404

    # Read single version
    res = get("/result/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("server", deepcopy(DEFINITIONS), indirect=["server"])
def test_delete(server):
    """Ensure that delete on empty store gives 404."""
    d: TestDefinition = server
    d.start()

    res = delete("/result/m0/v0")
    assert res.status_code == 404

    res = delete("/result/m0/v0/r0")
    assert res.status_code == 404

    res = delete("/result/m0/v0/r0/0")
    assert res.status_code == 404


@pytest.mark.parametrize("server", deepcopy(DEFINITIONS), indirect=["server"])
def test_write_read_delete(server):
    """Ensure that a written result can be read and deleted."""
    d: TestDefinition = server
    d.start()

    r = result_from("r0", "", [(0, {"hello": "world"})])

    res = post("/result/m0/v0", json=r.to_json())
    assert res.status_code == 200

    res = get("/result/m0/v0/r0")
    assert res.status_code == 200
    assert "results" in res.json()

    results = res.json()["results"]
    assert len(results) == 1

    result = Result.from_json(results[0])
    assert equal(r, result)

    res = delete("/result/m0/v0/r0")
    assert res.status_code == 200

    res = get("/result/m0/v0/r0")
    assert res.status_code == 404
