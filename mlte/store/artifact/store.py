"""
mlte/store/artifact/store.py

MLTE artifact store interface implementation.
"""

from __future__ import annotations

from typing import List, cast

from mlte.artifact.model import ArtifactModel
from mlte.context.model import (
    Model,
    ModelCreate,
    Namespace,
    NamespaceCreate,
    Version,
    VersionCreate,
)
from mlte.store.artifact.query import Query
from mlte.store.base import ManagedSession, Store, StoreSession

# -----------------------------------------------------------------------------
# ArtifactStore
# -----------------------------------------------------------------------------


class ArtifactStore(Store):
    """
    An abstract store.

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def session(self) -> ArtifactStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")


# -----------------------------------------------------------------------------
# ArtifactStoreSession
# -----------------------------------------------------------------------------


class ArtifactStoreSession(StoreSession):
    """The base class for all implementations of the MLTE artifact store session."""

    # -------------------------------------------------------------------------
    # Interface: Context
    # -------------------------------------------------------------------------

    def create_namespace(self, namespace: NamespaceCreate) -> Namespace:
        """
        Create a MLTE namespace.
        :param namespace: The namespace create model
        :return: The created namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_namespace(self, namespace_id: str) -> Namespace:
        """
        Read a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        :return: The namespace model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def list_namespaces(self) -> List[str]:
        """
        List all MLTE namespaces.
        :return: A collection of identifiers for all MLTE namespaces
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_namespace(self, namespace_id: str) -> Namespace:
        """
        Delete a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        :return: The deleted namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        """
        Create a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model: The model create model
        :return: The created model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Read a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :return: The model model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def list_models(self, namespace_id: str) -> List[str]:
        """
        List all MLTE models in the given namespace.
        :param namespace_id: The identifier for the namespace
        :return: A collection of identifiers for all MLTE models
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Delete a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :return: The deleted model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def create_version(
        self, namespace_id: str, model_id: str, version: VersionCreate
    ) -> Version:
        """
        Create a MLTE model version.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version: The version create model
        :return: The created version
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def list_versions(self, namespace_id: str, model_id: str) -> List[str]:
        """
        List all MLTE versions in the given namespace and model.
        :param namespace_id: the identifier for the namespace
        :param model_id: The identifier for the model
        :return: A collection of identifiers for all MLTE versions
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def read_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        """
        Read a MLTE model version.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :return: The version model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> Version:
        """
        Delete a MLTE model version.
        :param namespace_id: The identifier for the namespace
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

    def write_artifact(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact: ArtifactModel,
        *,
        force: bool = False,
        parents: bool = False,
    ) -> ArtifactModel:
        """
        Write an artifact.
        :param namespace_id: The identifier for the namespace
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
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        """
        Read an artifact.
        :param namespace_id: The identifier for the namespace
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
        namespace_id: str,
        model_id: str,
        version_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[ArtifactModel]:
        """
        Read artifacts withi limit and offset.
        :param namespace_id: The identifier for the namespace
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
        namespace_id: str,
        model_id: str,
        version_id: str,
        query: Query = Query(),
    ) -> List[ArtifactModel]:
        """
        Read a collection of artifacts, optionally filtered.
        :param namespace_id: The identifier for the namespace
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
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> ArtifactModel:
        """
        Delete an artifact.
        :param namespace_id: The identifier for the namespace
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
