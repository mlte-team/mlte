"""
Value persistence API for local filesystem.
"""

import json
from pathlib import Path
from typing import Optional, Set, Dict, Any

from .data_model import (
    Value,
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
      boundspec.json            <- ONLY present if BoundSpec is saved
      value_identifier0.json

The data for an individual value is then stored within a JSON file.
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


def _available_value_versions(value_path: Path) -> Set[int]:
    """
    Get the available versions for a value.
    :param value_path: The path to the value
    :type value_path: Path
    :return: The available versions for the value
    :rtype: Set[int]
    """
    with open(value_path.as_posix(), "r") as f:
        document = json.load(f)
        return set(e["version"] for e in document["versions"])


def _value_path(model_version_path: Path, value_identifier: str) -> Path:
    """
    Form the value path from model version path and value identifier.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param value_identifier: The identifier for the value
    :type value_identifier: str

    :return: The formatted value path
    :rtype: Path
    """
    return (
        model_version_path / value_identifier.replace(" ", "-")
    ).with_suffix(".json")


def _artifact_is_saved(model_version_path: Path, filename: str) -> bool:
    """
    Determine if an artifact is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if an artifact is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / filename).is_file()


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
        artifact: Dict[str, Any] = json.load(f)
        return artifact


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
    full_path = model_version_path / filename
    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)


# -----------------------------------------------------------------------------
# Read Value
# -----------------------------------------------------------------------------


def _read_value(value_path: Path, version: Optional[int] = None) -> Value:
    """
    Read the data for an individual value.
    :param value_path: The path to the value
    :type value_path: Path
    :param version: The (optional) version identifier
    :type version: Optional[int]
    :return: The read value
    :rtype: Value
    """
    with value_path.open("r") as f:
        value: Value = Value.from_json(json.load(f))

    # Ensure requested version is present
    assert (version is None) or (
        version in set(v.version for v in value.versions)
    ), "Broken invariant."

    # Filter to only include the version of interest
    # TODO(Kyle): Determine how we want to handle
    # multiversioning from user perspective / interface
    version = (
        max(_available_value_versions(value_path))
        if version is None
        else version
    )
    value.versions = [v for v in value.versions if v.version == version]
    return value


# -----------------------------------------------------------------------------
# Write Value
# -----------------------------------------------------------------------------


def _write_value(value_path: Path, value: Value, tag: Optional[str]):
    """
    Write a value to the file at `value_path`.
    :param value_path: The path to the value
    :type value_path: Path
    :param value: The value
    :type value: Value
    """
    if value_path.exists():
        new_version = max(_available_value_versions(value_path)) + 1

        # Read existing document
        with value_path.open("r") as f:
            mutating = Value.from_json(json.load(f))

        # Update tag
        mutating.tag = tag

        # Update value version
        mutating.versions.append(
            ResultVersion(version=new_version, data=value.versions[0].data)
        )

        # Persist updates
        with value_path.open("w") as f:
            json.dump(mutating.to_json(), f, indent=4)
    else:
        with value_path.open("w") as f:
            json.dump(value.to_json(), f, indent=4)


# -----------------------------------------------------------------------------
# API Interface
# -----------------------------------------------------------------------------


def read_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_version: Optional[int] = None,
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."
    _check_exists(root, model_identifier, model_version)

    version_path = root / model_identifier / model_version
    assert version_path.exists(), "Broken invariant."

    value_path = _value_path(version_path, value_identifier)
    if not value_path.exists():
        raise RuntimeError(
            f"Failed to read value, "
            f"value with identifier '{value_identifier}' not found."
        )

    if (
        value_version is not None
        and value_version not in _available_value_versions(value_path)
    ):
        raise RuntimeError(
            f"Failed to read value, "
            f"requested version {value_version} not found."
        )

    value = _read_value(value_path, value_version)
    assert len(value.versions) == 1, "Broken invariant."
    return value.versions[0].data


def write_value(
    uri: str,
    model_identifier: str,
    model_version: str,
    value_identifier: str,
    value_data: Dict[str, Any],
    value_tag: Optional[str],
):
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    # Construct internal data model
    value = Value.from_json(
        {
            "identifier": value_identifier,
            "tag": value_tag if value_tag is not None else "",
            "versions": [{"version": 0, "data": value_data}],
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

    value_path = _value_path(version_path, value_identifier)
    _write_value(value_path, value, value.tag)


def read_artifact(
    uri: str, model_identifier: str, model_version: str, filename: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    root = _parse_root_path(uri)
    assert root.exists(), "Broken precondition."

    _check_exists(root, model_identifier, model_version)

    model_version_path = root / model_identifier / model_version
    assert model_version_path.is_dir(), "Broken invariant."

    if not _artifact_is_saved(model_version_path, filename):
        raise RuntimeError("Failed to read artifact, artifact is not saved.")

    return _read_artifact(model_version_path, filename)


def write_artifact(
    uri: str,
    model_identifier: str,
    model_version: str,
    data: Dict[str, Any],
    filename: str,
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
    _write_artifact(model_version_path, filename, data)


def read_spec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return read_artifact(uri, model_identifier, model_version, SPEC_FILENAME)


def write_spec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    write_artifact(uri, model_identifier, model_version, data, SPEC_FILENAME)


def read_boundspec(
    uri: str, model_identifier: str, model_version: str
) -> Dict[str, Any]:
    """TODO(Kyle)"""
    return read_artifact(
        uri, model_identifier, model_version, BOUNDSPEC_FILENAME
    )


def write_boundspec(
    uri: str, model_identifier: str, model_version: str, data: Dict[str, Any]
):
    """TODO(Kyle)"""
    write_artifact(
        uri, model_identifier, model_version, data, BOUNDSPEC_FILENAME
    )


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
