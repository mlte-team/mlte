"""
mlte/store/artifact/underlying/memory.py

Implementation of in-memory artifact store.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Optional

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactLevel, ArtifactModel
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

        self.version_artifacts: dict[str, OrderedDict[str, ArtifactModel]] = {}
        """The version level artifacts, by version."""

    def get_all_artifacts(
        self, version_id: str
    ) -> OrderedDict[str, ArtifactModel]:
        """Returns all artifacts, from model and version level."""
        all_artifacts = self.artifacts.copy()
        all_artifacts.update(self.version_artifacts[version_id])
        return all_artifacts

    def get_artifact(
        self, version_id: str, artifact_id: str
    ) -> Optional[ArtifactModel]:
        """Gets an artifact from a model or version level."""
        # First check at the model level.
        if artifact_id in self.artifacts:
            return self.artifacts[artifact_id]
        else:
            # Then check at the version level.
            if artifact_id in self.version_artifacts[version_id]:
                return self.version_artifacts[version_id][artifact_id]
            else:
                return None

    def delete_artifact(
        self, artifact_id: str, version_id: Optional[str] = None
    ):
        """Removes the given artifact, from the given version, or from the model list."""
        if version_id:
            del self.version_artifacts[version_id][artifact_id]
        else:
            del self.artifacts[artifact_id]


class MemoryStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.models: dict[str, ModelArtifacts] = {}

    def add_artifact(
        self,
        artifact: ArtifactModel,
        model_id: str,
        version_id: str,
        level: ArtifactLevel,
    ):
        """Adds an artifact to the model or version level list."""
        if level == ArtifactLevel.MODEL:
            self.models[model_id].artifacts[
                artifact.header.identifier
            ] = artifact
        else:
            self.models[model_id].version_artifacts[version_id][
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
        if version.identifier in model.version_artifacts:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")

        model.version_artifacts[version.identifier] = OrderedDict()
        return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.version_artifacts:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return self._read_version(model_id, version_id)

    def list_versions(self, model_id: str) -> list[str]:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        return [version_id for version_id in model.version_artifacts.keys()]

    def delete_version(self, model_id: str, version_id: str) -> Version:
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")

        model = self.storage.models[model_id]
        if version_id not in model.version_artifacts:
            raise errors.ErrorNotFound(f"Version {version_id}")

        popped = self._read_version(model_id, version_id)
        del model.version_artifacts[version_id]
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
                for id in self.storage.models[model_id].version_artifacts.keys()
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
            version_id in self.storage.models[model_id].version_artifacts
        ), f"Version {version_id} not found int list for model {model_id}."
        return Version(identifier=version_id)

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

        artifact_id = artifact.header.identifier
        try:
            artifact = self._get_artifact(model_id, version_id, artifact_id)
            if not force:
                # If it exists and we are not "forcing" (overriting/editing), complain.
                raise errors.ErrorAlreadyExists(f"Artifact '{artifact_id}'")
        except errors.ErrorNotFound as ex:
            if "Artifact" in str(ex):
                # It is ok if artifact it was not found, it just means we are creating it.
                pass
            else:
                # If model or version were not found.
                raise ex

        self.storage.add_artifact(
            artifact, model_id, version_id, artifact.header.level
        )
        return artifact

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        return self._get_artifact(model_id, version_id, artifact_id)

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
        artifact = self.read_artifact(model_id, version_id, artifact_id)

        if artifact.header.level == ArtifactLevel.VERSION:
            self.storage.models[model_id].delete_artifact(
                artifact_id, version_id
            )
        else:
            self.storage.models[model_id].delete_artifact(artifact_id)

        return artifact

    def _get_artifact(
        self, model_id: str, version_id: str, artifact_id: str
    ) -> ArtifactModel:
        """
        Get the artifact from storage.
        :param model_id: The identifier for the model.
        :param version_id: The identifier for the version.
        :param artifact_id: The identifier for the artifact.
        :raises ErrorNotFound: If the model or version are not present.
        :return: The artifcat.
        """
        if model_id not in self.storage.models:
            raise errors.ErrorNotFound(f"Model {model_id}")
        model_artifacts = self.storage.models[model_id]

        if version_id not in model_artifacts.version_artifacts:
            raise errors.ErrorNotFound(
                f"Version: {version_id} for model {model_id}"
            )

        artifact = model_artifacts.get_artifact(version_id, artifact_id)
        if not artifact:
            raise errors.ErrorNotFound(
                f"Artifact: {artifact_id} for version {version_id} and model {model_id}"
            )
        else:
            return artifact

    def _get_artifacts(
        self, model_id: str, version_id: str
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
        model_artifacts = self.storage.models[model_id]

        if version_id not in model_artifacts.version_artifacts:
            raise errors.ErrorNotFound(f"Version {version_id}")

        return model_artifacts.get_all_artifacts(version_id)


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
