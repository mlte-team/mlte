"""
Result persistence API for local filesystem.
"""

import json
from pathlib import Path
from typing import Optional, Set, Dict, Any

from .data_model import (
    Result,
    ResultVersion,
)

# The prefix that indicates a local filesystem directory is used
LOCAL_URI_PREFIX = "local://"

# The name of the file that contains serialized specs
SPEC_FILENAME = "spec.json"
# The name of the file that contains serialized boundspecs
BOUNDSPEC_FILENAME = "boundspec.json"
# The name of the file that contains serialized bindings
BINDING_FILENAME = "binding.json"

"""
The overall structure for the directory hierarchy looks like:

root/
  model_identifier0/
    model_version0/
      spec.json                 <- ONLY present if Spec is saved
      binding.json              <- ONLY present if Binding is saved
      boundspec.json            <- ONLY present if BoundSpec is saved
      result_identifier0.json

The data for an individual result is then stored within a JSON file.
The structure of this JSON file looks like:

{
    "identifier": "...",
    "tag": "...",
    "versions": [
        {"version": 0, "data": ...}
        {"version": 1, "data": ...}
        ...
    ]
}
"""

# -----------------------------------------------------------------------------
# Parsing Helpers
# -----------------------------------------------------------------------------


def _parse_root_path(uri: str) -> Path:
    """
    Parse the root path for the backend from the URI.

    :param uri: The URI
    :type uri: str

    :return: The parsed path
    :rtype: Path
    """
    assert uri.startswith(LOCAL_URI_PREFIX), "Broken precondition."
    path = Path(uri[len(LOCAL_URI_PREFIX) :])
    if not path.exists():
        raise RuntimeError(
            f"Root path for local artifact store {path} does not exist."
        )
    return path


# -----------------------------------------------------------------------------
# Metadata
# -----------------------------------------------------------------------------


def _available_result_versions(result_path: Path) -> Set[int]:
    """
    Get the available versions for a result.
    :param result_path: The path to the result
    :type result_path: Path
    :return: The available versions for the result
    :rtype: Set[int]
    """
    with open(result_path.as_posix(), "r") as f:
        document = json.load(f)
        return set(e["version"] for e in document["versions"])


def _result_path(model_version_path: Path, result_identifier: str) -> Path:
    """
    Form the result path from model version path and result identifier.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param result_identifier: The identifier for the result
    :type result_identifier: str

    :return: The formatted result path
    :rtype: Path
    """
    return (
        model_version_path / result_identifier.replace(" ", "-")
    ).with_suffix(".json")


def _spec_is_saved(model_version_path: Path) -> bool:
    """
    Determine if a specification is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if a specification is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / SPEC_FILENAME).is_file()


def _binding_is_saved(model_version_path: Path) -> bool:
    """
    Determine if a binding is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if a binding is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / BINDING_FILENAME).is_file()


def _boundspec_is_saved(model_version_path: Path) -> bool:
    """
    Determine if a bound specification is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if a bound specification is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / BOUNDSPEC_FILENAME).is_file()


# -----------------------------------------------------------------------------
# Read / Write, for general artifacts.
# -----------------------------------------------------------------------------


def _read_artifact(model_version_path: Path, filename: str) -> Dict[str, Any]:
    """
    Read artifact data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param filename: The file name
    :type filename: str

    :return: The binding data
    :rtype: Dict[str, Any]
    """
    binding_path = model_version_path / filename
    assert binding_path.is_file(), "Broken invariant."

    with open(binding_path, "r") as f:
        result: Dict[str, Any] = json.load(f)
        return result


def _write_artifact(
    model_version_path: Path, filename: str, data: Dict[str, Any]
):
    """
    Write artifact data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param filename: The file name
    :type filename: str
    :param data: The binding data
    :type data: Dict[str, Any]
    """
    binding_path = model_version_path / filename
    with open(binding_path, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------------------------------------------
# Read Result
# -----------------------------------------------------------------------------


def _read_result(result_path: Path, version: Optional[int] = None) -> Result:
    """
    Read the data for an individual result.
    :param result_path: The path to the result
    :type result_path: Path
    :param version: The (optional) version identifier
    :type version: Optional[int]
    :return: The read result
    :rtype: Result
    """
    with result_path.open("r") as f:
        result: Result = Result.from_json(json.load(f))

    # Ensure requested version is present
    assert (version is None) or (
        version in set(v.version for v in result.versions)
    ), "Broken invariant."

    # Filter to only include the version of interest
    # TODO(Kyle): Determine how we want to handle
    # multiversioning from user perspective / interface
    version = (
        max(_available_result_versions(result_path))
        if version is None
        else version
    )
    result.versions = [v for v in result.versions if v.version == version]
    return result


# -----------------------------------------------------------------------------
# Write Result
# -----------------------------------------------------------------------------


def _write_result(result_path: Path, result: Result, tag: Optional[str]):
    """
    Write a result to the file at `result_path`.
    :param result_path: The path to the result
    :type result_path: Path
    :param result: The result
    :type result: Result
    """
    if result_path.exists():
        new_version = max(_available_result_versions(result_path)) + 1

        # Read existing document
        with result_path.open("r") as f:
            mutating = Result.from_json(json.load(f))

        # Update tag
        mutating.tag = tag

        # Update result version
        mutating.versions.append(
            ResultVersion(version=new_version, data=result.versions[0].data)
        )

        # Persist updates
        with result_path.open("w") as f:
            json.dump(mutating.to_json(), f, indent=4)
    else:
        with result_path.open("w") as f:
            json.dump(result.to_json(), f, indent=4)


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
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."
    _check_exists(root, model_identifier, model_version)

    version_path = root / model_identifier / model_version
    assert version_path.exists(), "Broken invariant."

    result_path = _result_path(version_path, result_identifier)
    if not result_path.exists():
        raise RuntimeError(
            f"Failed to read result, "
            f"result with identifier '{result_identifier}' not found."
        )

    if (
        result_version is not None
        and result_version not in _available_result_versions(result_path)
    ):
        raise RuntimeError(
            f"Failed to read result, "
            f"requested version {result_version} not found."
        )

    result = _read_result(result_path, result_version)
    assert len(result.versions) == 1, "Broken invariant."
    return result.versions[0].data


def write_result(
    uri: str,
    model_identifier: str,
    model_version: str,
    result_identifier: str,
    result_data: Dict[str, Any],
    result_tag: Optional[str],
):
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    # Construct internal data model
    result = Result.from_json(
        {
            "identifier": result_identifier,
            "tag": result_tag if result_tag is not None else "",
            "versions": [{"version": 0, "data": result_data}],
        }
    )

    # Create model directory
    model_path = root / model_identifier
    if not model_path.exists():
        model_path.mkdir()

    # Create version directory
    version_path = model_path / model_version
    if not version_path.exists():
        version_path.mkdir()

    result_path = _result_path(version_path, result_identifier)
    _write_result(result_path, result, result.tag)


def read_binding(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    _check_exists(root, model_identifier, model_version)

    model_version_path = root / model_identifier / model_version
    assert model_version_path.is_dir(), "Broken invariant."

    if not _binding_is_saved(model_version_path):
        raise RuntimeError("Failed to read binding, no binding is saved.")

    return _read_artifact(model_version_path, BINDING_FILENAME)


def write_binding(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    # Create model directory
    model_path = root / model_identifier
    if not model_path.exists():
        model_path.mkdir()

    # Create version directory
    version_path = model_path / model_version
    if not version_path.exists():
        version_path.mkdir()

    model_version_path = root / model_identifier / model_version
    _write_artifact(model_version_path, BINDING_FILENAME, data)


def read_spec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    _check_exists(root, model_identifier, model_version)

    model_version_path = root / model_identifier / model_version
    assert model_version_path.is_dir(), "Broken invariant."

    if not _spec_is_saved(model_version_path):
        raise RuntimeError("Failed to read binding, no binding is saved.")

    return _read_artifact(model_version_path, SPEC_FILENAME)


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    # Create model directory
    model_path = root / model_identifier
    if not model_path.exists():
        model_path.mkdir()

    # Create version directory
    version_path = model_path / model_version
    if not version_path.exists():
        version_path.mkdir()

    model_version_path = root / model_identifier / model_version
    _write_artifact(model_version_path, SPEC_FILENAME, data)


def read_boundspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    _check_exists(root, model_identifier, model_version)

    model_version_path = root / model_identifier / model_version
    assert model_version_path.is_dir(), "Broken invariant."

    if not _boundspec_is_saved(model_version_path):
        raise RuntimeError("Failed to read binding, no binding is saved.")

    return _read_artifact(model_version_path, BOUNDSPEC_FILENAME)


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    # Create model directory
    model_path = root / model_identifier
    if not model_path.exists():
        model_path.mkdir()

    # Create version directory
    version_path = model_path / model_version
    if not version_path.exists():
        version_path.mkdir()

    model_version_path = root / model_identifier / model_version
    _write_artifact(model_version_path, BOUNDSPEC_FILENAME, data)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


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
            f"Model with identifier '{model_identifier}' not found."
        )

    if model_version is None:
        return

    version_path = model_path / model_version
    if not version_path.exists():
        raise RuntimeError(
            f"Model version {model_version} "
            "for model {model_identifier} not found."
        )
