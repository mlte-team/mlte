"""
mlte/store/artifact/underlying/memory.py

Implementation of in-memory artifact store.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Optional

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.query import Query

# -----------------------------------------------------------------------------
# Data Structures
# -----------------------------------------------------------------------------


class ModelArtifacts:
    """A structure that contains model artifacts, at top level and version level."""

    def __init__(self) -> None:
        self.artifacts: OrderedDict[str, ArtifactModel] = OrderedDict()
        """The artifacts associated with the model only."""

        self.versions: dict[str, OrderedDict[str, ArtifactModel]] = {}
        """The versions in the model, along with the artifacts per version."""

    def get_all_artifacts(
        self, version_id: str
    ) -> OrderedDict[str, ArtifactModel]:
        """Returns all artifacts, from model and version level."""
        all_artifacts = self.artifacts.copy()
        all_artifacts.update(self.versions[version_id])
        return all_artifacts

    def delete_artifact(self, artifact_id: str, version_id: str):
        """Removes the given artifact, from the given version, or from the model list."""
        if version_id in self.versions:
            if artifact_id in self.versions[version_id]:
                del self.versions[version_id][artifact_id]
            else:
                # If the artifact was on in the provided version, assume it was in the model level ones.
                if artifact_id in self.artifacts:
                    del self.artifacts[artifact_id]


class MemoryStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.models: dict[str, ModelArtifacts] = {}

    def add_artifact(
        self, artifact: ArtifactModel, model_id: str, version_id: Optional[str]
    ):
        """Adds an artifact to the model or version level list."""
        if version_id:
            self.models[model_id].versions[version_id][
                artifact.header.identifier
            ] = artifact
        else:
            self.models[model_id].artifacts[
                artifact.header.identifier
            ] = artifact


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

    def create_model(self, model: Model) -> Model:
        if model.identifier in self.storage.models:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")
        self.storage.models[model.identifier] = ModelArtifacts()
        return Model(identifier=model.identifier, versions=[])

    def read_model(self, model_id: str) -> Model:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")
        return self._read_model(model_id)

    def list_models(self) -> list[str]:
        return [model_id for model_id in self.storage.models.keys()]

    def delete_model(self, model_id: str) -> Model:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        popped = self._read_model(model_id)
        del self.storage.models[model_id]
        return popped

    def create_version(self, model_id: str, version: Version) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version.identifier in model.versions:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")

        model.versions[version.identifier] = OrderedDict()
        return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return self._read_version(model_id, version_id)

    def list_versions(self, model_id: str) -> list[str]:
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
        assert (
            model_id in self.storage.models
        ), f"Model {model_id} not found in list of models."
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
        assert (
            model_id in self.storage.models
        ), f"Model {model_id} not found in list of models."
        assert (
            version_id in self.storage.models[model_id].versions
        ), f"Version {version_id} not found int list for model {model_id}."
        return Version(identifier=version_id)

    # -------------------------------------------------------------------------
    # Artifact
    # -------------------------------------------------------------------------

    def write_artifact(
        self,
        model_id: str,
        version_id: Optional[str],
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        if parents:
            storeutil.create_parents(self, model_id, version_id)

        artifacts = self._get_artifacts(model_id, version_id)

        if artifact.header.identifier in artifacts and not force:
            raise errors.ErrorAlreadyExists(
                f"Artifact '{artifact.header.identifier}'"
            )
        self.storage.add_artifact(artifact, model_id, version_id)
        return artifact

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifacts = self._get_artifacts(model_id, version_id)

        if artifact_id not in artifacts:
            raise errors.ErrorNotFound(f"Artifact '{artifact_id}'")
        return artifacts[artifact_id]

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[ArtifactModel]:
        artifacts = self._get_artifacts(model_id, version_id)
        return [artifact for artifact in artifacts.values()][
            offset : offset + limit
        ]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> list[ArtifactModel]:
        artifacts = self._get_artifacts(model_id, version_id)
        return [
            artifact
            for artifact in artifacts.values()
            if query.filter.match(artifact)
        ]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifacts = self._get_artifacts(model_id, version_id)

        if artifact_id not in artifacts:
            raise errors.ErrorNotFound(f"Artifact '{artifact_id}'")
        artifact = artifacts[artifact_id]

        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model: {model_id}")
        self.storage.models[model_id].delete_artifact(artifact_id, version_id)

        return artifact

    def _get_artifacts(
        self, model_id: str, version_id: Optional[str]
    ) -> OrderedDict[str, ArtifactModel]:
        """
        Get the artifcats from storage.
        :param model_id: The identifier for the model.
        :param version_id: The identifier for the version.
        :raises ErrorNotFound: If the model or version are not present.
        :return: The artifcats for this model and version, including model-level only.
        """
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")
        model = self.storage.models[model_id]

        if version_id and version_id not in model.versions:
            raise errors.ErrorNotFound(f"Version {version_id}")

        if not version_id:
            # Return model-level artifacts only.
            return model.artifacts
        else:
            return model.get_all_artifacts(version_id)


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
