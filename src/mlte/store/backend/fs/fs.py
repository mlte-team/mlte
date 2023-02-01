"""
Implementation of the filesystem-based backend store.
"""

import json
from pathlib import Path
from typing import List, Optional, Set, Dict, Any

from ..backend import Backend, BackendURI
from .data_model import (
    ModelIdentifier,
    ModelMetadata,
    ModelVersion,
    Result,
    ResultVersion,
)

# A sentinel value to indicate that the latest version should be read
# TODO(Kyle): Refactor this to something more type-safe
LATEST_VERSION = -1

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


def _parse_root_path(uri: BackendURI) -> Path:
    """
    Parse the root path for the backend from the URI.
    :param uri: The URI
    :type uri: BackendURI
    :return: The parsed path
    :rtype: Path
    """
    uristr: str = uri.uri
    assert uristr.startswith("fs://") or uristr.startswith(
        "local://"
    ), "Broken precondition."
    return (
        Path(uristr[len("fs://") :])
        if uristr.startswith("fs://")
        else Path(uristr[len("local://") :])
    )


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


def _available_results(version_path: Path) -> List[Path]:
    """
    Get all available results for a particular model version.
    :param version_path: The path to model version directory
    :type version_path: Path
    :return: A collection of paths for all results
    :rtype: List[Path]
    """
    return [x for x in version_path.glob("*") if x.is_file()]


def _available_model_versions(model_path: Path) -> List[Path]:
    """
    Get all available model versions for a particular model.
    :param model_path: The path to the model directory
    :type model_path: Path
    :return: A collection of paths to model versions
    :rtype: Set[Path]
    """
    return [x for x in model_path.glob("*") if x.is_dir()]


def _available_models(root_path: Path) -> List[Path]:
    """
    Get all available models in the store.
    :param root_path: The store root path
    :type root_path: Path
    :return: A collection of paths to models
    :rtype: Set[Path]
    """
    return [x for x in root_path.glob("*") if x.is_dir()]


def _read_tag(result_path: Path) -> str:
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
# Result
# -----------------------------------------------------------------------------


def _read_result(
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
        max(_available_result_versions(result_path))
        if version is None
        else version
    )

    versions = [v for v in result.versions if v.version == version]
    assert len(versions) == 1, "Broken invariant."

    data: Dict[str, Any] = versions[0].data
    return data


def _write_result(
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
        new_version = max(_available_result_versions(result_path)) + 1

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


def _delete_result_version(result_path: Path, version: int):
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


def _delete_result(result_path: Path):
    """
    Delete an individual result.
    """
    assert result_path.exists(), "Broken precondition."

    # Deleting all of the result versions implicitly deletes the result
    available_versions = _available_result_versions(result_path)
    assert len(available_versions) > 0, "Broken invariant."
    for version in available_versions:
        _delete_result_version(result_path, version)

    assert not result_path.exists(), "Broken postcondition."


def _delete_results(result_paths: List[Path]):
    """
    Delete a collection of results.
    """
    assert len(result_paths) > 0, "Broken precondition."
    for path in result_paths:
        _delete_result(path)

    assert all(not p.exists() for p in result_paths), "Broken postcondition."


def _propagate_deleted_result(model_path: Path, model_version: str):
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
    if len(_available_results(version_path)) == 0:
        version_path.rmdir()

    # If all model versions are deleted, remove the model
    if len(_available_model_versions(model_path)) == 0:
        model_path.rmdir()


# -----------------------------------------------------------------------------
# Read / Write Binding
# -----------------------------------------------------------------------------


def _read_binding(model_version_path: Path) -> Dict[str, Any]:
    """
    Read binding data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path

    :return: The binding data
    :rtype: Dict[str, Any]
    """
    binding_path = model_version_path / BINDING_FILENAME
    assert binding_path.is_file(), "Broken invariant."

    with open(binding_path, "r") as f:
        result: Dict[str, Any] = json.load(f)
        return result


def _write_binding(model_version_path: Path, data: Dict[str, Any]):
    """
    Write binding data for model version.

    :param model_version_path: The path to the model version
    :type model_version_path: Path
    :param data: The binding data
    :type data: Dict[str, Any]
    """
    binding_path = model_version_path / BINDING_FILENAME
    with open(binding_path, "w") as f:
        json.dump(data, f)


# -----------------------------------------------------------------------------
# Read / Write Spec
# -----------------------------------------------------------------------------


def _read_spec(model_version_path: Path) -> Dict[str, Any]:
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


def _write_spec(model_version_path: Path, data: Dict[str, Any]):
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
# BoundSpec
# -----------------------------------------------------------------------------


def _read_boundspec(model_version_path: Path) -> Dict[str, Any]:
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


def _write_boundspec(model_version_path: Path, data: Dict[str, Any]):
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


# -----------------------------------------------------------------------------
# FilesystemBackend
# -----------------------------------------------------------------------------


class FilesystemBackend(Backend):
    """
    The implementation of the filesystem-based backend.
    """

    def __init__(self, uri: BackendURI):
        """
        Initialize a new FilesystemBackendStore instance.
        :param uri: The URI that defines where the backend will store data
        :type uri: BackendURI
        """
        super().__init__(uri)

        # The root path to the data storage location
        self.root = _parse_root_path(self.uri)
        if not self.root.exists():
            raise RuntimeError(
                f"Root data storage location does not exist: {self.root}."
            )

    def read_model_metadata(
        self, model_identifier: Optional[str] = None
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""

        assert self.root.exists(), "Broken precondition."

        # Query all available models
        available_models = _available_models(self.root)

        if model_identifier is not None and not any(
            m.name == model_identifier for m in available_models
        ):
            raise RuntimeError(
                f"Model with identifier {model_identifier} does not exist."
            )

        # Collect results
        results: List[ModelMetadata] = []
        for model_path in available_models:
            available_versions = _available_model_versions(model_path)
            results.append(
                ModelMetadata(
                    identifier=ModelIdentifier(model_path.name),
                    versions=[ModelVersion(v.name) for v in available_versions],
                )
            )

        # Filter by queried model, if applicable
        results = (
            [r for r in results if r.identifier.identifier == model_identifier]
            if model_identifier is not None
            else results
        )
        return {"models": [r.to_json() for r in results]}

    def read_result(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        result_path = (version_path / result_identifier).with_suffix(".json")
        if not result_path.exists():
            raise RuntimeError(
                f"Failed to read result, result with identifier {result_identifier} not found."
            )

        if (
            result_version is not None
            and result_version not in _available_result_versions(result_path)
        ):
            raise RuntimeError(
                f"Failed to read result, requested version {result_version} not found."
            )

        return {"results": [_read_result(result_path, result_version)]}

    def read_results(
        self, model_identifier: str, model_version: str, tag: Optional[str]
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        # Query results and filter by tag, if applicable
        available_results = _available_results(version_path)
        if tag is not None:
            available_results = [
                p for p in available_results if _read_tag(p) == tag
            ]

        return {"results": [_read_result(p) for p in available_results]}

    def write_result(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_data: Dict[str, Any],
        result_tag: Optional[str],
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        # Create model directory
        model_path = self.root / model_identifier
        if not model_path.exists():
            model_path.mkdir()

        # Create version directory
        version_path = model_path / model_version
        if not version_path.exists():
            version_path.mkdir()

        result_path = (version_path / result_identifier).with_suffix(".json")
        _write_result(result_path, result_identifier, result_data, result_tag)

        return {"written": 1}

    def delete_result_version(
        self,
        model_identifier: str,
        model_version: str,
        result_identifier: str,
        result_version: int,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        result_path = (version_path / result_identifier).with_suffix(".json")
        if not result_path.exists():
            raise RuntimeError(
                f"Cannot delete result version, result with identifier {result_identifier} does not exist."
            )

        available_versions = _available_result_versions(result_path)
        if result_version not in available_versions:
            raise RuntimeError(
                f"Cannot delete result version, version {result_version} does not exist."
            )

        _delete_result_version(result_path, result_version)

        # Version deletion may have deleted the result entirety;
        # check to determine if this deletion must propagate
        _propagate_deleted_result(self.root / model_identifier, model_version)

        return {"deleted": 1}

    def delete_result(
        self, model_identifier: str, model_version: str, result_identifier: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        result_path = (version_path / result_identifier).with_suffix(".json")
        if not result_path.exists():
            raise RuntimeError(
                f"Cannot delete result version, result with identifier {result_identifier} does not exist."
            )

        _delete_result(result_path)

        # Result deletion may have removed last result in version
        _propagate_deleted_result(self.root / model_identifier, model_version)

        return {"deleted": 1}

    def delete_results(
        self,
        model_identifier: str,
        model_version: str,
        result_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        # Query all available results
        result_paths = _available_results(version_path)
        # Filter by tag, if applicable
        result_paths = (
            [p for p in result_paths if _read_tag(p) == result_tag]
            if result_tag is not None
            else result_paths
        )

        _delete_results(result_paths)

        # Result deletion may result in removal of model version
        _propagate_deleted_result(self.root / model_identifier, model_version)

        return {"deleted": len(result_paths)}

    def read_binding(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        model_version_path = self.root / model_identifier / model_version
        assert model_version_path.is_dir(), "Broken invariant."

        if not _binding_is_saved(model_version_path):
            raise RuntimeError("Failed to read binding, no binding is saved.")

        return {"binding": _read_binding(model_version_path)}

    def write_binding(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        # Create model directory
        model_path = self.root / model_identifier
        if not model_path.exists():
            model_path.mkdir()

        # Create version directory
        version_path = model_path / model_version
        if not version_path.exists():
            version_path.mkdir()

        model_version_path = self.root / model_identifier / model_version
        _write_binding(model_version_path, data)

        return {"written": 1}

    def read_spec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        model_version_path = self.root / model_identifier / model_version
        assert model_version_path.is_dir(), "Broken invariant."

        if not _spec_is_saved(model_version_path):
            raise RuntimeError("Failed to read binding, no binding is saved.")

        return {"spec": _read_spec(model_version_path)}

    def write_spec(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        # Create model directory
        model_path = self.root / model_identifier
        if not model_path.exists():
            model_path.mkdir()

        # Create version directory
        version_path = model_path / model_version
        if not version_path.exists():
            version_path.mkdir()

        model_version_path = self.root / model_identifier / model_version
        _write_spec(model_version_path, data)

        return {"written": 1}

    def read_boundspec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        model_version_path = self.root / model_identifier / model_version
        assert model_version_path.is_dir(), "Broken invariant."

        if not _boundspec_is_saved(model_version_path):
            raise RuntimeError("Failed to read binding, no binding is saved.")

        return {"boundspec": _read_boundspec(model_version_path)}

    def write_boundspec(
        self, model_identifier: str, model_version: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        # Create model directory
        model_path = self.root / model_identifier
        if not model_path.exists():
            model_path.mkdir()

        # Create version directory
        version_path = model_path / model_version
        if not version_path.exists():
            version_path.mkdir()

        model_version_path = self.root / model_identifier / model_version
        _write_boundspec(model_version_path, data)

        return {"written": 1}

    def _check_exists(
        self, model_identifier: str, model_version: Optional[str] = None
    ):
        """
        Check if data is available for a particular model and version.
        :param model_identifier: The model identifier
        :type model_identifier: str
        :param model_version: The model version
        :type model_version: Optional[str]
        """
        model_path = self.root / model_identifier
        if not model_path.exists():
            raise RuntimeError(
                f"Model with identifier {model_identifier} not found."
            )

        if model_version is None:
            return

        version_path = model_path / model_version
        if not version_path.exists():
            raise RuntimeError(
                f"Model version {model_version} for model {model_identifier} not found."
            )


# -----------------------------------------------------------------------------
# FilesystemBackendBuilder
# -----------------------------------------------------------------------------


class FilesystemBackendBuilder:
    """A builder for the FilesystemBackendStore."""

    def __init__(self):
        pass

    def with_uri(self, uri: BackendURI):
        self.uri = uri
        return self

    def build(self) -> FilesystemBackend:
        return FilesystemBackend(uri=self.uri)
