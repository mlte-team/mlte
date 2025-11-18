"""MLTE artifact store interface session implementation."""

from __future__ import annotations

import time
from typing import Any, Optional, cast

import mlte.store.error as errors
from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, Version
from mlte.store.base import (
    ManagedSession,
    ResourceMapper,
    StoreSession,
    StoreURI,
)


class ArtifactStoreSession(StoreSession):
    """The base class for all implementations of the MLTE artifact store session."""

    model_mapper: ModelMapper
    """Mapper for the model resource."""

    version_mapper: VersionMapper
    """Mapper for the version resource."""

    artifact_mapper: ArtifactMapper
    """Mapper for the artifact resource."""

    def create_parents(self, model_id: str, version_id: str) -> None:
        """
        Create organizational elements within this store. If they exist, this operation is a noop.
        :param model_id: The model identifier
        :param version_id: The version identifier
        """
        try:
            self.model_mapper.create(Model(identifier=model_id))
        except errors.ErrorAlreadyExists:
            pass

        try:
            self.version_mapper.create(Version(identifier=version_id), model_id)
        except errors.ErrorAlreadyExists:
            pass


class ManagedArtifactSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> ArtifactStoreSession:
        return cast(ArtifactStoreSession, self.session)


class ModelMapper(ResourceMapper):
    """An interface for mapping CRUD actions to models."""

    def create(self, new_model: Model, context: Any = None) -> Model:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, model_id: str, context: Any = None) -> Model:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, context: Any = None) -> list[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, model: Model, context: Any = None) -> Model:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, model_id: str, context: Any = None) -> Model:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)


class VersionMapper(ResourceMapper):
    """An interface for mapping CRUD actions to versions."""

    def create(self, new_version: Version, model_id: str) -> Version:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, version_id: str, model_id: str) -> Version:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, model_id: str) -> list[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, version: Version, model_id: str) -> Version:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, version_id: str, model_id: str) -> Version:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)


class ArtifactMapper(ResourceMapper):
    """An interface for mapping CRUD actions to artifacts."""

    def create(
        self, new_artifact: ArtifactModel, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        try:
            # If artifact to create exists, complain.
            _ = self.read(new_artifact.header.identifier, model_and_version)
            raise errors.ErrorAlreadyExists(
                f"Artifact '{new_artifact.header.identifier}' already exists."
            )
        except errors.ErrorNotFound:
            # We expect it not to be found when creating.
            return self._store_artifact(new_artifact, model_and_version)

    def read(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self, model_and_version: tuple[str, str]) -> list[str]:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(
        self, artifact: ArtifactModel, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        # Check to see if the artifact exists before editing it, which will throw an error if it doesn't.
        _ = self.read(artifact.header.identifier, model_and_version)
        return self._store_artifact(artifact, model_and_version)

    def delete(
        self, artifact_id: str, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)

    def _add_header_data(
        self, artifact: ArtifactModel, user: Optional[str]
    ) -> ArtifactModel:
        """Adds time and creator data to model."""
        artifact.header.timestamp = int(time.time())
        artifact.header.creator = user
        return artifact

    def write_artifact_with_header(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        user: Optional[str] = None,
    ) -> ArtifactModel:
        """
        Write an artifact, generating the timestamp and adding creator. Internally calls the actual write_artifact implementation.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The artifact
        :param force: Overwrite an artifact if it already exists
        for artifact should be implictly created (default: False)
        :param user: The username of the user executing this action.
        """
        artifact = self._add_header_data(artifact, user)
        return self.write_artifact(
            model_id,
            version_id,
            artifact,
            force=force,
        )

    def write_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
    ) -> ArtifactModel:
        """
        Write an artifact.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The artifact
        :param force: Overwrite an artifact if it already exists
        for artifact should be implictly created (default: False)
        """
        artifact_id = artifact.header.identifier
        try:
            artifact = self.read(artifact_id, (model_id, version_id))
            if not force:
                # If it exists and we are not "forcing" (overriting/editing), complain it already exists.
                raise errors.ErrorAlreadyExists(
                    f"Artifact '{artifact_id}' (force param prevents overwriting it)"
                )
            return self.edit(artifact, (model_id, version_id))
        except errors.ErrorNotFound as ex:
            if "Artifact" in str(ex):
                # This means artifact did not exist; we want to create it.
                return self.create(artifact, (model_id, version_id))
            else:
                # If model or version were not found, we can't move fowrad.
                raise ex

    def _store_artifact(
        self, artifact: ArtifactModel, model_and_version: tuple[str, str]
    ) -> ArtifactModel:
        """Writes an artifact to the store."""
        raise NotImplementedError(ResourceMapper.NOT_IMPLEMENTED_ERROR_MSG)
