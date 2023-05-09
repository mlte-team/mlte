"""
store/backend/fs/fs.py

Implementation of the filesystem-based backend store.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Dict, Any

from mlte.store.backend import (
    BackendEngine,
    SessionHandle,
    BackendURI,
    BackendType,
)
from mlte.store.backend.fs.data_model import (
    ModelIdentifier,
    ModelMetadata,
    ModelVersion,
)
import mlte.store.backend.fs.storage as storage


"""
The overall structure for the directory hierarchy looks like:

root/
  model_identifier0/
    model_version0/
      spec.json                 <- ONLY present if Spec is saved
      validatedspec.json            <- ONLY present if ValidatedSpec is saved
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
# FilesystemBackendEngine
# -----------------------------------------------------------------------------


class FilesystemBackendEngine(BackendEngine):
    """
    The implementation of the filesystem-based backend engine.
    """

    def __init__(self, *, uri: BackendURI):
        """
        Initialize a new FilesystemBackendStore instance.
        :param uri: The URI that defines where the backend will store data
        :type uri: BackendURI
        """
        assert uri.type == BackendType.FS, "Broken precondition."
        super().__init__(uri=uri)

        # The root path to the data storage location
        self.root = _parse_root_path(self.uri)
        if not self.root.exists():
            raise RuntimeError(
                f"Root data storage location does not exist: {self.root}."
            )

    def handle(self) -> FilesystemSessionHandle:
        """
        Return a new handle to the backend session.
        :return: The handle
        :rtype: FilesystemSessionHandle
        """
        return FilesystemSessionHandle(root=self.root)

    @staticmethod
    def create(uri: BackendURI) -> FilesystemBackendEngine:
        """
        Create a new filesystem backend engine.
        :param uri: The backend URI
        :type uri: BackendURI
        :return: The instance
        :rtype: FilesystemBackendEngine
        """
        return FilesystemBackendEngine(uri=uri)


# -----------------------------------------------------------------------------
# FilesystemSessionHandle
# -----------------------------------------------------------------------------


class FilesystemSessionHandle(SessionHandle):
    def __init__(self, *, root: Path):
        """
        Initialize a new FilesystemSessionHandle.
        :param root: The root storage location
        :type root: Path
        """
        self.root = root

    def close(self) -> None:
        """Close the session handle."""
        # No-op for filesystem backend
        pass

    def read_model_metadata(
        self, model_identifier: Optional[str] = None
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""

        assert self.root.exists(), "Broken precondition."

        # Query all available models
        available_models = storage.available_models(self.root)

        if model_identifier is not None and not any(
            m.name == model_identifier for m in available_models
        ):
            raise RuntimeError(
                f"Model with identifier {model_identifier} does not exist."
            )

        # Collect models
        models: List[ModelMetadata] = []
        for model_path in available_models:
            available_versions = storage.available_model_versions(model_path)
            models.append(
                ModelMetadata(
                    identifier=ModelIdentifier(model_path.name),
                    versions=[ModelVersion(v.name) for v in available_versions],
                )
            )

        # Filter by queried model, if applicable
        models = (
            [m for m in models if m.identifier.identifier == model_identifier]
            if model_identifier is not None
            else models
        )
        return {"models": [r.to_json() for r in models]}

    def read_value(
        self,
        model_identifier: str,
        model_version: str,
        value_identifier: str,
        value_version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        value_path = (version_path / value_identifier).with_suffix(".json")
        if not value_path.exists():
            raise RuntimeError(
                f"Failed to read value, value with identifier {value_identifier} not found."
            )

        if (
            value_version is not None
            and value_version
            not in storage.available_value_versions(value_path)
        ):
            raise RuntimeError(
                f"Failed to read value, requested version {value_version} not found."
            )

        return {"values": [storage.read_value(value_path, value_version)]}

    def read_values(
        self, model_identifier: str, model_version: str, tag: Optional[str]
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        # Query values and filter by tag, if applicable
        available_values = storage.available_valuess(version_path)
        if tag is not None:
            available_values = [
                p for p in available_values if storage.read_tag(p) == tag
            ]

        return {"values": [storage.read_value(p) for p in available_values]}

    def write_value(
        self,
        model_identifier: str,
        model_version: str,
        value_identifier: str,
        value_data: Dict[str, Any],
        value_tag: Optional[str] = None,
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

        value_path = (version_path / value_identifier).with_suffix(".json")
        storage.write_value(value_path, value_identifier, value_data, value_tag)

        return {"written": 1}

    def delete_value_version(
        self,
        model_identifier: str,
        model_version: str,
        value_identifier: str,
        value_version: int,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        value_path = (version_path / value_identifier).with_suffix(".json")
        if not value_path.exists():
            raise RuntimeError(
                f"Cannot delete value version, value with identifier {value_identifier} does not exist."
            )

        available_versions = storage.available_value_versions(value_path)
        if value_version not in available_versions:
            raise RuntimeError(
                f"Cannot delete value version, version {value_version} does not exist."
            )

        storage.delete_value_version(value_path, value_version)

        # Version deletion may have deleted the value entirety;
        # check to determine if this deletion must propagate
        storage.propagate_deleted_value(
            self.root / model_identifier, model_version
        )

        return {"deleted": 1}

    def delete_value(
        self, model_identifier: str, model_version: str, value_identifier: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        value_path = (version_path / value_identifier).with_suffix(".json")
        if not value_path.exists():
            raise RuntimeError(
                f"Cannot delete value version, value with identifier {value_identifier} does not exist."
            )

        storage.delete_value(value_path)

        # Value deletion may have removed last value in version
        storage.propagate_deleted_value(
            self.root / model_identifier, model_version
        )

        return {"deleted": 1}

    def delete_values(
        self,
        model_identifier: str,
        model_version: str,
        value_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."
        self._check_exists(model_identifier, model_version)

        version_path = self.root / model_identifier / model_version
        assert version_path.exists(), "Broken invariant."

        # Query all available values
        value_paths = storage.available_valuess(version_path)
        # Filter by tag, if applicable
        value_paths = (
            [p for p in value_paths if storage.read_tag(p) == value_tag]
            if value_tag is not None
            else value_paths
        )

        storage.delete_values(value_paths)

        # Value deletion may value in removal of model version
        storage.propagate_deleted_value(
            self.root / model_identifier, model_version
        )

        return {"deleted": len(value_paths)}

    def read_spec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        model_version_path = self.root / model_identifier / model_version
        assert model_version_path.is_dir(), "Broken invariant."

        if not storage.spec_is_saved(model_version_path):
            raise RuntimeError("Failed to read spec, no spec is saved.")

        return {"spec": storage.read_spec(model_version_path)}

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
        storage.write_spec(model_version_path, data)

        return {"written": 1}

    def read_validatedspec(
        self, model_identifier: str, model_version: str
    ) -> Dict[str, Any]:
        """TODO(Kyle)"""
        assert self.root.exists(), "Broken precondition."

        self._check_exists(model_identifier, model_version)

        model_version_path = self.root / model_identifier / model_version
        assert model_version_path.is_dir(), "Broken invariant."

        if not storage.validatedspec_is_saved(model_version_path):
            raise RuntimeError(
                "Failed to read validatedspec, no validatedpsec is saved."
            )

        return {"validatedspec": storage.read_validatedspec(model_version_path)}

    def write_validatedspec(
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
        storage.write_validatedspec(model_version_path, data)

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
