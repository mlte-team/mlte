"""
mlte/store/artifact/store.py

MLTE artifact store interface implementation.
"""

from __future__ import annotations

import time
from typing import List, Optional, cast

from mlte.artifact.model import ArtifactModel
from mlte.context.model import Model, ModelCreate, Version, VersionCreate
from mlte.store.base import ManagedSession, Store, StoreSession
from mlte.store.query import Query

# -----------------------------------------------------------------------------
# ArtifactStore
# -----------------------------------------------------------------------------


class ArtifactStore(Store):
    """
    An abstract artifact store.

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def session(self) -> ArtifactStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Can't call session on a base Store.")


# -----------------------------------------------------------------------------
# ArtifactStoreSession
# -----------------------------------------------------------------------------


class ArtifactStoreSession(StoreSession):
    """The base class for all implementations of the MLTE artifact store session."""

    # -------------------------------------------------------------------------
    # Interface: Context
    # -------------------------------------------------------------------------

    def create_model(self, model: ModelCreate) -> Model:
        """
        Create a MLTE model.
        :param model: The model data to create the model
        :return: The created model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_model(self, model_id: str) -> Model:
        """
        Read a MLTE model.
        :param model_id: The identifier for the model
        :return: The model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def list_models(self) -> List[str]:
        """
        List all MLTE models in the store.
        :return: A collection of identifiers for all MLTE models
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_model(self, model_id: str) -> Model:
        """
        Delete a MLTE model.
        :param model_id: The identifier for the model
        :return: The deleted model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def create_version(self, model_id: str, version: VersionCreate) -> Version:
        """
        Create a MLTE model version.
        :param model_id: The identifier for the model
        :param version: The version create model
        :return: The created version
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def list_versions(self, model_id: str) -> List[str]:
        """
        List all MLTE versions in the given model.
        :param model_id: The identifier for the model
        :return: A collection of identifiers for all MLTE versions
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_version(self, model_id: str, version_id: str) -> Version:
        """
        Read a MLTE model version.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :return: The version model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_version(self, model_id: str, version_id: str) -> Version:
        """
        Delete a MLTE model version.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :return: The deleted version
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    # -------------------------------------------------------------------------
    # Interface: Artifact
    # -------------------------------------------------------------------------

    def write_artifact_with_header(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
        user: Optional[str] = None,
    ) -> ArtifactModel:
        """
        Write an artifact, generating the timestamp and adding creator. Internally calls the actual write_artifact implementation.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The artifact
        :param force: Overwrite an artifact if it already exists
        :param parents: Indicates whether organizational elements
        for artifact should be implictly created (default: False)
        """
        artifact.header.timestamp = int(time.time())
        artifact.header.creator = user
        return self.write_artifact(
            model_id,
            version_id,
            artifact,
            force=force,
            parents=parents,
        )

    def write_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        """
        Write an artifact.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The artifact
        :param force: Overwrite an artifact if it already exists
        :param parents: Indicates whether organizational elements
        for artifact should be implictly created (default: False)
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        """
        Read an artifact.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact_id: The artifact identifier
        :return: The artifact
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_artifacts(
        self,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        """
        Read artifacts withi limit and offset.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param limit: The limit on artifacts to read
        :param offset: The offset on artifacts to read
        :return: The read artifacts
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def search_artifacts(
        self,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        """
        Read a collection of artifacts, optionally filtered.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param query: The artifact query to apply
        :return: A collection of artifacts that satisfy the filter
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_artifact(
        self,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        """
        Delete an artifact.
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact_id: The artifact identifier
        :return: The deleted artifact
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )


class ManagedArtifactSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> ArtifactStoreSession:
        return cast(ArtifactStoreSession, self.session)
