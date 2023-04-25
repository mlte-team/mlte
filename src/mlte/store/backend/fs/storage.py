"""
store/backend/fs/storage.py

Storage helpers for filesystem backend.
"""

import json

from pathlib import Path
from typing import Set, List, Optional, Dict, Any

from .data_model import Result, ResultVersion

# A sentinel value to indicate that the latest version should be read
# TODO(Kyle): Refactor this to something more type-safe
LATEST_VERSION = -1

# The name of the file that contains serialized specs
SPEC_FILENAME = "spec.json"
# The name of the file that contains serialized boundspecs
BOUNDSPEC_FILENAME = "boundspec.json"
# The name of the file that contains serialized bindings
BINDING_FILENAME = "binding.json"

# -----------------------------------------------------------------------------
# Query Metadata
# -----------------------------------------------------------------------------


def available_result_versions(result_path: Path) -> Set[int]:
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


def available_results(version_path: Path) -> List[Path]:
    """
    Get all available results for a particular model version.
    :param version_path: The path to model version directory
    :type version_path: Path
    :return: A collection of paths for all results
    :rtype: List[Path]
    """
    return [x for x in version_path.glob("*") if x.is_file()]


def available_model_versions(model_path: Path) -> List[Path]:
    """
    Get all available model versions for a particular model.
    :param model_path: The path to the model directory
    :type model_path: Path
    :return: A collection of paths to model versions
    :rtype: Set[Path]
    """
    return [x for x in model_path.glob("*") if x.is_dir()]


def available_models(root_path: Path) -> List[Path]:
    """
    Get all available models in the store.
    :param root_path: The store root path
    :type root_path: Path
    :return: A collection of paths to models
    :rtype: Set[Path]
    """
    return [x for x in root_path.glob("*") if x.is_dir()]


def read_tag(result_path: Path) -> str:
    """
    Read the tag for an individual result.
    :param result_path: The path to the result
    :type result_path: Path
    :return: The tag
    :rtype: str
    """
    with result_path.open("r") as f:
        document = json.load(f)
        result: str = document["tag"]
        return result


def spec_is_saved(model_version_path: Path) -> bool:
    """
    Determine if a specification is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if a specification is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / SPEC_FILENAME).is_file()


def binding_is_saved(model_version_path: Path) -> bool:
    """
    Determine if a binding is saved to the store for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: `True` if a binding is present, `False` otherwise
    :rtype: bool
    """
    assert model_version_path.is_dir(), "Broken precondition."
    return (model_version_path / BINDING_FILENAME).is_file()


def boundspec_is_saved(model_version_path: Path) -> bool:
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
# Read / Write Result
# -----------------------------------------------------------------------------


def read_value(
    result_path: Path, version: Optional[int] = None
) -> Dict[str, Any]:
    """
    Read the data for an individual result.
    :param result_path: The path to the result
    :type result_path: Path
    :param version: The (optional) version identifier
    :type version: Optional[int]
    :return: The read result
    :rtype: Dict[str, Any]
    """
    with result_path.open("r") as f:
        result = Result.from_json(json.load(f))

    # Ensure requested version is present
    assert (version is None) or (
        version in set(v.version for v in result.versions)
    ), "Broken invariant."

    # Filter to only include the version of interest
    # TODO(Kyle): Determine how we want to handle
    # multiversioning from user perspective / interface
    version = (
        max(available_result_versions(result_path))
        if version is None
        else version
    )

    versions = [v for v in result.versions if v.version == version]
    assert len(versions) == 1, "Broken invariant."

    data: Dict[str, Any] = versions[0].data
    return data


def write_value(
    result_path: Path, identifier: str, data: Dict[str, Any], tag: Optional[str]
):
    """
    Write a result to the file at `result_path`.
    :param result_path: The path to the result
    :param identifier: The result identifier
    :type identifier: str
    :type result_path: Path
    :param data: The result data
    :type data: Dict[str, Any]
    :param tag: The result tag
    :type tag: Optional[str]
    """
    if result_path.exists():
        new_version = max(available_result_versions(result_path)) + 1

        # Read existing document
        with result_path.open("r") as f:
            mutating = Result.from_json(json.load(f))

        # Update tag
        mutating.tag = tag

        # Update result version
        mutating.versions.append(ResultVersion(version=new_version, data=data))

        # Persist updates
        with result_path.open("w") as f:
            json.dump(mutating.to_json(), f)
    else:
        result = Result(
            identifier=identifier, versions=[ResultVersion(0, data)], tag=tag
        )
        with result_path.open("w") as f:
            json.dump(result.to_json(), f)


def delete_result_version(result_path: Path, version: int):
    """
    Delete an individual version for a result.
    :param result_path: The path to the result
    :type result_path: Path
    :param version: The target version
    :type version: int
    """
    assert result_path.exists(), "Broken precondition."
    with result_path.open("r") as f:
        result = Result.from_json(json.load(f))

    # Update versions data
    assert version in set(
        v.version for v in result.versions
    ), "Broken invariant."
    result.versions = [v for v in result.versions if v.version != version]

    # If no versions remain, delete this result
    if len(result.versions) == 0:
        result_path.unlink()
        return

    # Otherwise, versions remain, write updated content
    with result_path.open("w") as f:
        json.dump(result.to_json(), f)


def delete_result(result_path: Path):
    """
    Delete an individual result.
    """
    assert result_path.exists(), "Broken precondition."

    # Deleting all of the result versions implicitly deletes the result
    available_versions = available_result_versions(result_path)
    assert len(available_versions) > 0, "Broken invariant."
    for version in available_versions:
        delete_result_version(result_path, version)

    assert not result_path.exists(), "Broken postcondition."


def delete_results(result_paths: List[Path]):
    """
    Delete a collection of results.
    """
    assert len(result_paths) > 0, "Broken precondition."
    for path in result_paths:
        delete_result(path)

    assert all(not p.exists() for p in result_paths), "Broken postcondition."


def propagate_deleted_result(model_path: Path, model_version: str):
    """
    Propagate the deletion of one or more results to higher-level structures.
    :param model_path: The path to the model directory
    :type model_path: Path
    :param model_version: The string identifier for model version
    :type model_version: str
    """
    assert model_path.exists(), "Broken precondition."

    # If all results are deleted, remove the model version
    version_path = model_path / model_version
    if len(available_results(version_path)) == 0:
        version_path.rmdir()

    # If all model versions are deleted, remove the model
    if len(available_model_versions(model_path)) == 0:
        model_path.rmdir()


# -----------------------------------------------------------------------------
# Read / Write Spec
# -----------------------------------------------------------------------------


def read_spec(model_version_path: Path) -> Dict[str, Any]:
    """
    Read specification data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: The specification data
    :rtype: Dict[str, Any]
    """
    spec_path = model_version_path / SPEC_FILENAME
    assert spec_path.is_file(), "Broken invariant."

    with open(spec_path, "r") as f:
        result: Dict[str, Any] = json.load(f)
        return result


def write_spec(model_version_path: Path, data: Dict[str, Any]):
    """
    Write specification data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param data: The specification data
    :type data: Dict[str, Any]
    """
    spec_path = model_version_path / SPEC_FILENAME
    with open(spec_path, "w") as f:
        json.dump(data, f)


# -----------------------------------------------------------------------------
# Read / Write BoundSpec
# -----------------------------------------------------------------------------


def read_boundspec(model_version_path: Path) -> Dict[str, Any]:
    """
    Read bound specification data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: The bound specification data
    :rtype: Dict[str, Any]
    """
    spec_path = model_version_path / BOUNDSPEC_FILENAME
    assert spec_path.is_file(), "Broken invariant."

    with open(spec_path, "r") as f:
        result: Dict[str, Any] = json.load(f)
        return result


def write_boundspec(model_version_path: Path, data: Dict[str, Any]):
    """
    Write bound specification data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param data: The specification data
    :type data: Dict[str, Any]
    """
    spec_path = model_version_path / BOUNDSPEC_FILENAME
    with open(spec_path, "w") as f:
        json.dump(data, f)
