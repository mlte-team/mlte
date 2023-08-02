"""
mlte/api/local/api.py

Value persistence API for local filesystem.
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
# Value
# -----------------------------------------------------------------------------


def read_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_value(
        model_identifier, model_version, value_identifier, value_version
    )
    assert "values" in document, "Broken invariant."
    assert len(document["values"]) == 1, "Broken invariant."
    value: Dict[str, Any] = document["values"][0]
    return value


def write_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_data: Dict[str, Any],
    value_tag: Optional[str],
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_value(
        model_identifier,
        model_version,
        value_identifier,
        value_data,
        value_tag,
    )
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
# Validated Specification
# -----------------------------------------------------------------------------


def read_validatedspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.read_validatedspec(model_identifier, model_version)
    assert "validatedspec" in document, "Broken invariant."
    validatedspec: Dict[str, Any] = document["validatedspec"]
    return validatedspec


def write_validatedspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    handle = _get_backend_handle(uri)
    document = handle.write_validatedspec(model_identifier, model_version, data)
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
