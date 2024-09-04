"""
mlte/store/artifact/underlying/memory.py

Implementation of in-memory artifact store.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict, List

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.query import Query

# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class VersionWithArtifacts:
    """A structure that combines a version with the artifacts it contains."""

    def __init__(self, *, identifier: str) -> None:
        self.identifier = identifier
        """The version identifier."""

        self.artifacts: OrderedDict[str, ArtifactModel] = OrderedDict()
        """The artifacts associated with the version."""


class ModelWithVersions:
    """A structure that combines a model with the versions it contains."""

    def __init__(self, *, identifier: str) -> None:
        self.identifier = identifier
        """The model identifier."""

        self.versions: Dict[str, VersionWithArtifacts] = {}
        """The collection of versions in the model."""


class MemoryStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.models: Dict[str, ModelWithVersions] = {}


# -----------------------------------------------------------------------------
# InMemoryStoreSession
# -----------------------------------------------------------------------------


class InMemoryStoreSession(ArtifactStoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, *, storage: MemoryStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        # NOTE(Kyle): Closing an in-memory session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        if model.identifier in self.storage.models:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")
        self.storage.models[model.identifier] = ModelWithVersions(
            identifier=model.identifier
        )
        return Model(identifier=model.identifier, versions=[])

    def read_model(self, model_id: str) -> Model:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")
        return self._read_model(model_id)

    def list_models(self) -> List[str]:
        return [model_id for model_id in self.storage.models.keys()]

    def delete_model(self, model_id: str) -> Model:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        popped = self._read_model(model_id)
        del self.storage.models[model_id]
        return popped

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version.identifier in model.versions:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")

        model.versions[version.identifier] = VersionWithArtifacts(
            identifier=version.identifier
        )
        return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return self._read_version(model_id, version_id)

    def list_versions(self, model_id: str) -> List[str]:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        return [version_id for version_id in model.versions.keys()]

    def delete_version(self, model_id: str, version_id: str) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        popped = self._read_version(model_id, version_id)
        del model.versions[version_id]
        return popped

    def _read_model(self, model_id: str) -> Model:
        """
        Lazily construct a Model object on read.
        :param model_id: The model identifier
        :return: The model object
        """
        assert model_id in self.storage.models, "Broken precondition."
        return Model(
            identifier=model_id,
            versions=[
                self._read_version(model_id, id)
                for id in self.storage.models[model_id].versions.keys()
            ],
        )

    def _read_version(self, model_id: str, version_id: str) -> Version:
        """
        Lazily construct a Version object on read.
        :param model_id: The model identifier
        :param version_id: The version identifier
        :return: The version object
        """
        assert model_id in self.storage.models, "Broken precondition."
        assert (
            version_id in self.storage.models[model_id].versions
        ), "Broken precondition."
        return Version(
            identifier=self.storage.models[model_id]
            .versions[version_id]
            .identifier
        )

    # -------------------------------------------------------------------------
    # Artifact
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        if parents:
            storeutil.create_parents(self, model_id, version_id)

        version = self._get_version_with_artifacts(model_id, version_id)

        if artifact.header.identifier in version.artifacts and not force:
            raise errors.ErrorAlreadyExists(
                f"Artifact '{artifact.header.identifier}'"
            )
        version.artifacts[artifact.header.identifier] = artifact
        return artifact

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        version = self._get_version_with_artifacts(model_id, version_id)

        if artifact_id not in version.artifacts:
            raise errors.ErrorNotFound(f"Artifact '{artifact_id}'")
        return version.artifacts[artifact_id]

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        version = self._get_version_with_artifacts(model_id, version_id)
        return [artifact for artifact in version.artifacts.values()][
            offset : offset + limit
        ]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        version = self._get_version_with_artifacts(model_id, version_id)
        return [
            artifact
            for artifact in version.artifacts.values()
            if query.filter.match(artifact)
        ]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        version = self._get_version_with_artifacts(model_id, version_id)

        if artifact_id not in version.artifacts:
            raise errors.ErrorNotFound(f"Artifact '{artifact_id}'")
        artifact = version.artifacts[artifact_id]
        del version.artifacts[artifact_id]
        return artifact

    def _get_version_with_artifacts(
        self, model_id: str, version_id: str
    ) -> VersionWithArtifacts:
        """
        Get a version with artifacts from storage.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the version
        :raises ErrorNotFound: If the required structural elements are not present
        :return: The version with associated artifacts
        """
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return model.versions[version_id]


class InMemoryStore(ArtifactStore):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = MemoryStorage()
        """The underlying storage for the store."""

    def session(self) -> InMemoryStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryStoreSession(storage=self.storage)
