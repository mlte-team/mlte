"""
Result persistence API for local filesystem.
"""

from pathlib import Path
from typing import Optional, Dict, Any

from ...backend import BackendURI, BackendType
from ...backend.fs import FilesystemBackend

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
    backend = _get_backend(uri)
    document = backend.read_result(
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
    backend = _get_backend(uri)
    document = backend.write_result(
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
    backend = _get_backend(uri)
    document = backend.read_binding(model_identifier, model_version)
    assert "binding" in document, "Broken precondition."
    binding: Dict[str, Any] = document["binding"]
    return binding


def write_binding(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    document = backend.write_binding(model_identifier, model_version, data)
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
    backend = _get_backend(uri)
    document = backend.read_spec(model_identifier, model_version)
    assert "spec" in document, "Broken invariant."
    spec: Dict[str, Any] = document["spec"]
    return spec


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    document = backend.write_spec(model_identifier, model_version, data)
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
    backend = _get_backend(uri)
    document = backend.read_boundspec(model_identifier, model_version)
    assert "boundspec" in document, "Broken invariant."
    boundspec: Dict[str, Any] = document["boundspec"]
    return boundspec


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
) -> int:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    document = backend.write_boundspec(model_identifier, model_version, data)
    assert "written" in document, "Broken invariant."
    assert document["written"] == 1, "Broken invariant."
    count: int = document["written"]
    return count


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def _get_backend(uri: str) -> FilesystemBackend:
    """Instantiate a backend instance."""
    parsed = BackendURI.from_string(uri)
    assert parsed.type == BackendType.FS, "Broken invariant."
    return FilesystemBackend(parsed)


def _check_exists(
    root: Path, model_identifier: str, model_version: Optional[str] = None
):
    """
    Check if data is available for a particular model and version.
    :param root: The root path
    :type root: Path
    :param model_identifier: The model identifier
    :type model_identifier: str
    :param model_version: The model version
    :type model_version: Optional[str]
    """
    model_path = root / model_identifier
    if not model_path.exists():
        raise RuntimeError(
            f"Model with identifier {model_identifier} not found."
        )

    if model_version is None:
        return

    version_path = model_path / model_version
    if not version_path.exists():
        raise RuntimeError(
            f"Model version {model_version} "
            "for model {model_identifier} not found."
        )
