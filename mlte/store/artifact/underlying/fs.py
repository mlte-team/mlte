"""Implementation of local file system artifact store."""

from __future__ import annotations

from typing import Any

import mlte.store.error as errors
from mlte.artifact.model import ArtifactLevel, ArtifactModel
from mlte.context.model import Model, Version
from mlte.store.artifact.store import ArtifactStore
from mlte.store.artifact.store_session import (
    ArtifactMapper,
    ArtifactStoreSession,
    ModelMapper,
    VersionMapper,
)
from mlte.store.base import StoreURI
from mlte.store.common.fs_storage import FileSystemStorage
from mlte.store.validators.composite_validator import CompositeValidator

# -----------------------------------------------------------------------------
# LocalFileSystemStore
# -----------------------------------------------------------------------------


class LocalFileSystemStore(ArtifactStore):
    """A local file system implementation of the MLTE artifact store."""

    BASE_MODELS_FOLDER = "models"
    """Base folder to store models in."""

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
        # TODO: This is the problem line causing things to reinstantiate and then lose my validators
        return LocalFileSystemStoreSession(storage=self.storage, validators=self.validators)


# -----------------------------------------------------------------------------
# LocalFileSystemStoreSession
# -----------------------------------------------------------------------------


class LocalFileSystemStoreSession(ArtifactStoreSession):
    """A local file-system implementation of the MLTE artifact store."""

    def __init__(self, storage: FileSystemStorage, validators: CompositeValidator) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.version_mapper = FileSystemVersionMapper(storage=storage)
        """The mapper to version CRUD."""

        self.model_mapper = FileSystemModelMapper(
            storage=storage, version_mapper=self.version_mapper
        )
        """The mapper to model CRUD."""

        self.artifact_mapper = FileSystemArtifactMapper(storage=storage, validators=validators)
        """The mapper to artifact CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass


# -------------------------------------------------------------------------
# Resource Group: Models.
# -------------------------------------------------------------------------


class FileSystemModelMapper(ModelMapper):
    """File storage mapper for the model resource."""

    def __init__(
        self,
        *,
        storage: FileSystemStorage,
        version_mapper: FileSystemVersionMapper,
    ) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.version_mapper = version_mapper
        """A reference to the version mapper."""

    def create(self, model: Model, context: Any = None) -> Model:
        try:
            self.storage.create_resource_group(model.identifier)
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Model {model.identifier}")

        return Model(identifier=model.identifier, versions=[])

    def read(self, model_id: str, context: Any = None) -> Model:
        self._ensure_model_exists(model_id)
        return Model(
            identifier=model_id,
            versions=self.version_mapper.list_details(model_id),
        )

    def list(self, context: Any = None) -> list[str]:
        return self.storage.list_resource_groups()

    def delete(self, model_id: str, context: Any = None) -> Model:
        model = self.read(model_id)
        self.storage.delete_resource_group(model_id)
        return model

    def _ensure_model_exists(self, model_id: str) -> None:
        """Throws an ErrorNotFound if the given model  does not exist."""
        if not self.storage.exists_resource_group(model_id):
            raise errors.ErrorNotFound(f"Model {model_id}")


# -------------------------------------------------------------------------
# Resource Group: Versions.
# -------------------------------------------------------------------------


class FileSystemVersionMapper(VersionMapper):
    """File storage mapper for the version resource."""

    def __init__(self, *, storage: FileSystemStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, version: Version, model_id: str) -> Version:
        self._ensure_model_exists(model_id)

        try:
            self.storage.create_resource_group(version.identifier, [model_id])
        except FileExistsError:
            raise errors.ErrorAlreadyExists(f"Version {version.identifier}")
        return Version(identifier=version.identifier)

    def read(self, version_id: str, model_id: str) -> Version:
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(version_id, model_id)
        return Version(identifier=version_id)

    def list(self, model_id: str) -> list[str]:
        self._ensure_model_exists(model_id)
        return self.storage.list_resource_groups([model_id])

    def delete(self, version_id: str, model_id: str) -> Version:
        version = self.read(version_id, model_id)
        self.storage.delete_resource_group(version_id, [model_id])
        return version

    def _ensure_model_exists(self, model_id: str) -> None:
        """Throws an ErrorNotFound if the given model  does not exist."""
        if not self.storage.exists_resource_group(model_id):
            raise errors.ErrorNotFound(f"Model {model_id}")

    def _ensure_version_exists(self, version_id: str, model_id: str) -> None:
        """Throws an ErrorNotFound if the given version of the given model does not exist."""
        if not self.storage.exists_resource_group(version_id, [model_id]):
            raise errors.ErrorNotFound(
                f"Version {version_id} in model {model_id}"
            )


# -------------------------------------------------------------------------
# Artifact mapper
# -------------------------------------------------------------------------


class FileSystemArtifactMapper(ArtifactMapper):
    """File storage mapper for the artifact resource."""

    def __init__(self, *, storage: FileSystemStorage, validators: CompositeValidator) -> None:
        self.storage = storage
        """A reference to underlying storage."""

        self.validators: CompositeValidator = validators
        """A reference to the store validators."""

    def read(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        group_ids = self._get_artifact_groups(model_id, version_id, artifact_id)
        return ArtifactModel(
            **self.storage.read_resource(artifact_id, group_ids)
        )

    def list(self, model_and_version: tuple[str, str]) -> list[str]:
        model_id, version_id = model_and_version
        return self._get_artifact_ids(model_id, version_id)

    def delete(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        model_id, version_id = model_and_version
        artifact = self.read(artifact_id, (model_id, version_id))
        group_ids = self._get_artifact_groups(model_id, version_id, artifact_id)
        self.storage.delete_resource(artifact_id, group_ids)
        return artifact

    # -------------------------------------------------------------------------
    # Internal helpers.
    # -------------------------------------------------------------------------

    def _store_artifact(
        self,
        artifact: ArtifactModel,
        model_and_version: tuple[str, str],
    ) -> ArtifactModel:
        """Writes artifact to storage."""

        # Only store in version subgroup if it was requested.
        model_id, version_id = model_and_version
        group_ids = [model_id]
        if artifact.header.level == ArtifactLevel.VERSION:
            group_ids += [version_id]

        try:
            self.storage.write_resource(
                artifact.header.identifier,
                artifact.to_json(),
                group_ids,
            )
            return self.read(artifact.header.identifier, (model_id, version_id))
        except FileNotFoundError:
            raise errors.ErrorNotFound(
                f"Model or version not found: {model_id}, {version_id}"
            )

    def _get_artifact_groups(
        self, model_id: str, version_id: str, artifact_id: str
    ) -> list[str]:  # type: ignore
        """Finds at what level an artifact is stored, and returns a list of those groups."""
        # First trying at the model/version level, then at the model level.
        group_ids = [model_id, version_id]
        try:
            self.storage.ensure_resource_exists(artifact_id, group_ids)
        except errors.ErrorNotFound:
            try:
                group_ids = [model_id]
                self.storage.ensure_resource_exists(artifact_id, group_ids)
            except errors.ErrorNotFound:
                raise errors.ErrorNotFound(f"Artifact {artifact_id}")

        return group_ids

    def _get_artifact_ids(self, model_id: str, version_id: str) -> list[str]:  # type: ignore
        """Returns all artifact ids from both model/version levels, and just model level."""
        self._ensure_model_exists(model_id)
        self._ensure_version_exists(version_id, model_id)
        version_artifacts = []
        version_artifacts = self.storage.list_resources(
            group_ids=[model_id, version_id]
        )
        model_artifacts = self.storage.list_resources(group_ids=[model_id])
        return version_artifacts + model_artifacts

    def _ensure_model_exists(self, model_id: str) -> None:
        """Throws an ErrorNotFound if the given model does not exist."""
        if not self.storage.exists_resource_group(model_id):
            raise errors.ErrorNotFound(f"Model {model_id}")

    def _ensure_version_exists(self, version_id: str, model_id: str) -> None:
        """Throws an ErrorNotFound if the given version of the given model does not exist."""
        if not self.storage.exists_resource_group(version_id, [model_id]):
            raise errors.ErrorNotFound(
                f"Version {version_id} in model {model_id}"
            )
