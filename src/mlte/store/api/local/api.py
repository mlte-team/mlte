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
# API Interface
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
    return backend.read_result(
        model_identifier, model_version, result_identifier, result_version
    )


def write_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_data: Dict[str, Any],
    result_tag: Optional[str],
):
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.write_result(
        model_identifier,
        model_version,
        result_identifier,
        result_data,
        result_tag,
    )


def read_binding(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.read_binding(model_identifier, model_version)


def write_binding(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.write_binding(model_identifier, model_version, data)


def read_spec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.read_spec(model_identifier, model_version)


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.write_spec(model_identifier, model_version, data)


def read_boundspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.read_boundspec(model_identifier, model_version)


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    backend = _get_backend(uri)
    return backend.write_boundspec(model_identifier, model_version, data)


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
