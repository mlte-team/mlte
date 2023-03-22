"""
Unit tests for backend implementation.
"""

from copy import deepcopy

import pytest

from mlte.store.backend.initialize import initialize_backend
from .support.backend import TestDefinition
from .support.backend.fs import (
    construct_uri,
    create_temporary_directory,
    delete_temporary_directory,
)


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

DEFINITIONS = [
    TestDefinition(
        "fs",
        "artifact:uri",
        {},
        [create_temporary_directory, construct_uri],
        [delete_temporary_directory],
    )
]


@pytest.fixture()
def backend(request):
    """A fixture to perform setup and teardown."""
    d: TestDefinition = request.param
    try:
        d.setup()
        yield d
    finally:
        d.teardown()


@pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
def test_initialize(backend):
    d: TestDefinition = backend
    _ = initialize_backend(d.uri, d.environment)
    assert True


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     written = store.write_result(
#         "m0", "v0", result_from("r0", "", [(0, {"0": "0"})])
#     )
#     assert written == 1


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_read(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     r0 = result_from("r0", "", [(0, {"hello": "world"})])
#     written = store.write_result("m0", "v0", r0)
#     assert written == 1

#     r1 = store.read_result("m0", "v0", "r0")
#     assert equal(r0, r1)


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_read_latest(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))
#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"1": "1"})]))
#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"2": "2"})]))

#     r = store.read_result("m0", "v0", "r0")
#     e = result_from(
#         "r0", "", [(0, {"0": "0"}), (1, {"1": "1"}), (2, {"2": "2"})]
#     )
#     assert equal(r, e)


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_read_version(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     v0 = result_from("r0", "", [(0, {"0": "0"})])
#     store.write_result("m0", "v0", v0)

#     v1 = result_from("r0", "", [(1, {"1": "1"})])
#     store.write_result("m0", "v0", v1)

#     v2 = result_from("r0", "", [(2, {"2": "2"})])
#     store.write_result("m0", "v0", v2)

#     for vid, exp in zip([0, 1, 2], [v0, v1, v2]):
#         r = store.read_result("m0", "v0", "r0", vid)
#         assert equal(r, exp)


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_read_bad_version(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))
#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))

#     with pytest.raises(RuntimeError):
#         store.read_result("m0", "v0", "r0", 2)


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_read_nonexistent_model(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     with pytest.raises(RuntimeError):
#         _ = store.read_result("fakemodel", "fakeversion", "fakeresult")


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_delete_result_version(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))
#     _ = store.read_result("m0", "v0", "r0")

#     store.delete_result_version("m0", "v0", "r0", 0)

#     # Reading exact version should fail
#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r0", 0)

#     # Reading latest should fail
#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r0")


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_write_delete_result(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))
#     _ = store.read_result("m0", "v0", "r0")

#     store.delete_result("m0", "v0", "r0")

#     # Reading latest should fail
#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r0")


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_delete_results(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "", [(0, {"0": "0"})]))
#     store.write_result("m0", "v0", result_from("r1", "", [(0, {"1": "1"})]))

#     store.delete_results("m0", "v0")

#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r0")
#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r1")


# @pytest.mark.parametrize("backend", deepcopy(DEFINITIONS), indirect=["backend"])
# def test_delete_results_with_tag(backend):
#     d: TestDefinition = backend
#     store = initialize_backend_store(d.uri, d.environment)

#     store.write_result("m0", "v0", result_from("r0", "t0", [(0, {"0": "0"})]))
#     store.write_result("m0", "v0", result_from("r1", "t0", [(0, {"1": "1"})]))
#     store.write_result("m0", "v0", result_from("r2", "", [(0, {"2": "2"})]))

#     store.delete_results("m0", "v0", "t0")

#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r0")
#     with pytest.raises(RuntimeError):
#         _ = store.read_result("m0", "v0", "r1")

#     _ = store.read_result("m0", "v0", "r2")
