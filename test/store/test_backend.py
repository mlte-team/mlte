"""
Unit tests for backend implementation.
"""

import pytest
from typing import Any

from mlte.store.backend import SessionHandle
from .fixture.backend import fs_handle  # noqa


# -----------------------------------------------------------------------------
# Test Definitions
# -----------------------------------------------------------------------------

"""
This list contains the global collection of test handles.
However, because we cannot directly parametrize a test with
a fixture function, we specify via strings and then use the
`request` fixture to translate this into the actual fixture.
"""
HANDLES = ["fs_handle"]

# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------


def result_from(*args: Any) -> Any:
    """Dummy function."""
    return 0


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_initialize(handle_fixture: str, request: pytest.FixtureRequest):
    _: SessionHandle = request.getfixturevalue(handle_fixture)
    assert True


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write(handle_fixture: str, request: pytest.FixtureRequest):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)
    _ = handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    assert True


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_read(handle_fixture: str, request: pytest.FixtureRequest):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)
    r0 = result_from("r0", "", [(0, {"hello": "world"})])
    _ = handle.write_value("m0", "v0", "r0", r0)
    assert True

    _ = handle.read_value("m0", "v0", "r0")
    assert True


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_read_latest(handle_fixture: str, request: pytest.FixtureRequest):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"1": "1"})])
    )
    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"2": "2"})])
    )

    _ = handle.read_value("m0", "v0", "r0")
    _ = result_from(
        "r0", "", [(0, {"0": "0"}), (1, {"1": "1"}), (2, {"2": "2"})]
    )
    assert True


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_read_version(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    v0 = result_from("r0", "", [(0, {"0": "0"})])
    handle.write_value("m0", "v0", "r0", v0)

    v1 = result_from("r0", "", [(1, {"1": "1"})])
    handle.write_value("m0", "v0", "r0", v1)

    v2 = result_from("r0", "", [(2, {"2": "2"})])
    handle.write_value("m0", "v0", "r0", v2)

    for vid, exp in zip([0, 1, 2], [v0, v1, v2]):
        _ = handle.read_value("m0", "v0", "r0", vid)
        assert True


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_read_bad_version(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )

    with pytest.raises(RuntimeError):
        handle.read_value("m0", "v0", "r0", 2)


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_read_nonexistent_model(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    with pytest.raises(RuntimeError):
        _ = handle.read_value("fakemodel", "fakeversion", "fakeresult")


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_delete_result_version(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    _ = handle.read_value("m0", "v0", "r0")

    handle.delete_value_version("m0", "v0", "r0", 0)

    # Reading exact version should fail
    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r0", 0)

    # Reading latest should fail
    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r0")


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_write_delete_result(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    _ = handle.read_value("m0", "v0", "r0")

    handle.delete_value("m0", "v0", "r0")

    # Reading latest should fail
    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r0")


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_delete_results(handle_fixture: str, request: pytest.FixtureRequest):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "", [(0, {"0": "0"})])
    )
    handle.write_value(
        "m0", "v0", "r1", result_from("r1", "", [(0, {"1": "1"})])
    )

    handle.delete_values("m0", "v0")

    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r0")
    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r1")


@pytest.mark.skip(reason="Awaiting refactor for internal artifact format.")
@pytest.mark.parametrize("handle_fixture", HANDLES)
def test_delete_results_with_tag(
    handle_fixture: str, request: pytest.FixtureRequest
):
    handle: SessionHandle = request.getfixturevalue(handle_fixture)

    handle.write_value(
        "m0", "v0", "r0", result_from("r0", "t0", [(0, {"0": "0"})])
    )
    handle.write_value(
        "m0", "v0", "r1", result_from("r1", "t0", [(0, {"1": "1"})])
    )
    handle.write_value(
        "m0", "v0", "r2", result_from("r2", "", [(0, {"2": "2"})])
    )

    handle.delete_values("m0", "v0", "t0")

    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r0")
    with pytest.raises(RuntimeError):
        _ = handle.read_value("m0", "v0", "r1")

    _ = handle.read_value("m0", "v0", "r2")
