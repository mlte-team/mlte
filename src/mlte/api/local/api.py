"""
Result persistence API for local filesystem.
"""

from typing import Optional, Dict, Any

from mlte.store.backend import BackendURI, BackendType
from mlte.store.backend.fs import (
    FilesystemBackendEngine,
    FilesystemSessionHandle,
)

# The prefix that indicates a local filesystem directory is used
LOCAL_URI_PREFIX = "local://"

# -----------------------------------------------------------------------------
# Result
# -----------------------------------------------------------------------------


def read_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_result(
        model_identifier, model_version, result_identifier, result_version
    )
    assert "results" in document, "Broken invariant."
    assert len(document["results"]) == 1, "Broken invariant."
    result: Dict[str, Any] = document["results"][0]
    return result


def write_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_data: Dict[str, Any],
    result_tag: Optional[str],
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_result(
        model_identifier,
        model_version,
        result_identifier,
        result_data,
        result_tag,
    )
    assert "written" in document, "Broken invariant."
    assert document["written"] == 1, "Broken invariant."
    count: int = document["written"]
    return count


# -----------------------------------------------------------------------------
# Binding
# -----------------------------------------------------------------------------


def read_binding(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_binding(model_identifier, model_version)
    assert "binding" in document, "Broken precondition."
    binding: Dict[str, Any] = document["binding"]
    return binding


def write_binding(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_binding(model_identifier, model_version, data)
    assert "written" in document, "Broken invariant."
    assert document["written"] == 1, "Broken invariant."
    count: int = document["written"]
    return count


# -----------------------------------------------------------------------------
# Specification
# -----------------------------------------------------------------------------


def read_spec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_spec(model_identifier, model_version)
    assert "spec" in document, "Broken invariant."
    spec: Dict[str, Any] = document["spec"]
    return spec


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_spec(model_identifier, model_version, data)
    assert "written" in document, "Broken invariant."
    assert document["written"] == 1, "Broken invariant"
    count: int = document["written"]
    return count


# -----------------------------------------------------------------------------
# Bound Specification
# -----------------------------------------------------------------------------


def read_boundspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_boundspec(model_identifier, model_version)
    assert "boundspec" in document, "Broken invariant."
    boundspec: Dict[str, Any] = document["boundspec"]
    return boundspec


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_boundspec(model_identifier, model_version, data)
    assert "written" in document, "Broken invariant."
    assert document["written"] == 1, "Broken invariant."
    count: int = document["written"]
    return count


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_backend_handle(uri: str) -> FilesystemSessionHandle:
    """
    Initialize a filesystem backend instance and return a handle to it.
    :param uri: The URI string
    :type uri: str
    :return: The session handle
    :rtype: FilesystemSessionHandle
    """
    parsed = BackendURI.from_string(uri)
    assert parsed.type == BackendType.FS, "Broken invariant."
    return FilesystemBackendEngine.create(parsed).handle()
