"""
mlte/store/artifact/underlying/fs.py

Implementation of local file system artifact store.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

import mlte.store.artifact.util as storeutil
import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.artifact.store import ArtifactStore, ArtifactStoreSession
from mlte.store.base import StoreURI
from mlte.store.common.fs_storage import FileSystemStorage
from mlte.store.query import Query

# -----------------------------------------------------------------------------
# LocalFileSystemStore
# -----------------------------------------------------------------------------


class LocalFileSystemStore(ArtifactStore):
    """A local file system implementation of the MLTE artifact store."""

    BASE_MODELS_FOLDER = "models"
    """Base fodler to store models in."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = FileSystemStorage(
            uri=uri, sub_folder=self.BASE_MODELS_FOLDER
        )
        """The underlying storage for the store."""

    def session(self) -> LocalFileSystemStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return LocalFileSystemStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# LocalFileSystemStoreSession
# -----------------------------------------------------------------------------


class LocalFileSystemStoreSession(ArtifactStoreSession):
    """A local file-system implementation of the MLTE artifact store."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass

    # -------------------------------------------------------------------------
    # Structural Elements
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        try:
            self.storage.create_folder(
                Path(self.storage.base_path, model.identifier)
            )
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")

        return Model(identifier=model.identifier, versions=[])

    def read_model(self, model_id: str) -> Model:
        self._ensure_model_exists(model_id)
        return self._read_model(model_id)

    def list_models(self) -> List[str]:
        return [
            str(model_path.relative_to(self.storage.base_path))
            for model_path in self.storage.list_folders(self.storage.base_path)
        ]

    def delete_model(self, model_id: str) -> Model:
        self._ensure_model_exists(model_id)
        model = self._read_model(model_id)
        self.storage.delete_folder(Path(self.storage.base_path, model_id))
        return model

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        self._ensure_model_exists(model_id)

        try:
            self.storage.create_folder(
                Path(self.storage.base_path, model_id, version.identifier)
            )
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")
        return Version(identifier=version.identifier)

    def read_version(self, model_id: str, version_id: str) -> Version:
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(model_id, version_id)

        return self._read_version(model_id, version_id)

    def list_versions(self, model_id: str) -> List[str]:
        self._ensure_model_exists(model_id)

        model_path = Path(self.storage.base_path, model_id)
        return [
            str(version_path.relative_to(model_path))
            for version_path in self.storage.list_folders(model_path)
        ]

    def delete_version(self, model_id: str, version_id: str) -> Version:
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(model_id, version_id)

        version = self._read_version(model_id, version_id)
        self.storage.delete_folder(
            Path(self.storage.base_path, model_id, version_id)
        )
        return version

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _ensure_model_exists(self, model_id: str) -> None:
        """Throws an ErrorNotFound if the given model  does not exist."""
        if not Path(self.storage.base_path, model_id).exists():
            raise errors.ErrorNotFound(f"Model {model_id}")

    def _ensure_version_exists(self, model_id: str, version_id: str) -> None:
        """Throws an ErrorNotFound if the given version of the given model does not exist."""
        if not Path(self.storage.base_path, model_id, version_id).exists():
            raise errors.ErrorNotFound(
                f"Version {version_id} in model {model_id}"
            )

    def _read_model(self, model_id: str) -> Model:
        """
        Lazily construct a Model object on read.
        :param model_id: The model identifier
        :return: The model object
        """
        self._ensure_model_exists(model_id)
        return Model(
            identifier=model_id,
            versions=[
                self._read_version(model_id, id)
                for id in self.list_versions(model_id)
            ],
        )

    def _read_version(self, model_id: str, version_id: str) -> Version:
        """
        Lazily construct a Version object on read.
        :param model_id: The model identifier
        :param version_id: The version identifier
        :return: The version object
        """
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(model_id, version_id)
        return Version(identifier=version_id)

    # -------------------------------------------------------------------------
    # Artifacts
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

        artifacts = self._get_version_artifacts(model_id, version_id)
        if artifact.header.identifier in artifacts and not force:
            raise errors.ErrorAlreadyExists(
                f"Artifact '{artifact.header.identifier}'"
            )

        self.storage.write_json_to_file(
            self._artifact_path(
                model_id, version_id, artifact.header.identifier
            ),
            artifact.model_dump(),
        )
        return artifact

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifacts = self._get_version_artifacts(model_id, version_id)

        self._ensure_artifact_exists(artifact_id, artifacts)
        return ArtifactModel(
            **self.storage.read_json_file(
                self._artifact_path(model_id, version_id, artifact_id)
            )
        )

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        artifacts = self._get_version_artifacts(model_id, version_id)
        return [
            ArtifactModel(
                **self.storage.read_json_file(
                    self._artifact_path(model_id, version_id, artifact_id)
                )
            )
            for artifact_id in artifacts
        ][offset : offset + limit]

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        artifacts = self.read_artifacts(model_id, version_id)
        return [
            artifact for artifact in artifacts if query.filter.match(artifact)
        ]

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        artifact = self.read_artifact(model_id, version_id, artifact_id)
        self.storage.delete_file(
            self._artifact_path(
                model_id, version_id, artifact.header.identifier
            )
        )
        return artifact

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _ensure_artifact_exists(
        self, artifact_id: str, artifacts: List[str]
    ) -> None:
        """Throws an ErrorNotFound if the given artifact does not exist."""
        if artifact_id not in artifacts:
            raise errors.ErrorNotFound(f"Artifact {artifact_id}")

    def _get_version_artifacts(
        self, model_id: str, version_id: str
    ) -> List[str]:
        """
        Get artifacts for a version from storage.
         :param model_id: The identifier for the model
        :param version_id: The identifier for the version
        :raises ErrorNotFound: If the required structural elements are not present
        :return: The associated artifacts
        """
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(model_id, version_id)

        return [
            a.stem
            for a in self.storage.list_json_files(
                self._base_artifact_path(model_id, version_id)
            )
        ]

    def _base_artifact_path(self, model_id: str, version_id: str) -> Path:
        """
        Format a local FS path to a version of a model .
        :param model_id: The model identifier
        :param version_id: The version identifier
        :return: The formatted path
        """
        return Path(self.storage.base_path, model_id, version_id)

    def _artifact_path(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ):
        """
        Formats a local FS path to an artifact.
        :param model_id: The model identifier
        :param version_id: The version identifier
        :param artifact_id: The artifact identifier
        :return: The formatted path
        """
        return Path(
            self._base_artifact_path(model_id, version_id),
            self.storage.add_extension(artifact_id),
        )
