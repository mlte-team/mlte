"""
mlte/store/backend/store.py

MLTE artifact store interface implementation.
"""

from __future__ import annotations

from enum import Enum

from mlte.context.model import (
    Namespace,
    NamespaceCreate,
    Model,
    ModelCreate,
    Version,
    VersionCreate,
)
from mlte.artifact.model import ArtifactModel
from mlte.store.query import ArtifactFilter, AllFilter

# -----------------------------------------------------------------------------
# StoreType
# -----------------------------------------------------------------------------


class StoreType(Enum):
    """Represents the type of the MLTE artifact store."""

    LOCAL_MEMORY = "local_memory"
    """An in-memory store implementation."""

    LOCAL_FILESYSTEM = "local_filesystem"
    """A local filesystem implementation."""

    REMOTE_HTTP = "remote_http"
    """A remote HTTP implementation."""


# -----------------------------------------------------------------------------
# StoreURI
# -----------------------------------------------------------------------------


class StoreURI:
    """Represents the URI for an artifact store instance."""

    def __init__(self, uri: str, type: StoreType):
        """
        Initialize a StoreURI instance.
        :param uri: The URI
        :param type: The type of the backend store
        """
        self.uri = uri
        """The string that represents the URI."""

        self.type = type
        """The type identifier for the URI."""

    @staticmethod
    def from_string(uri: str) -> StoreURI:
        """
        Parse a StoreURI from a string.
        :param uri: The URI
        :return: The parsed StoreURI
        """
        if uri.startswith("memory://"):
            return StoreURI(uri, StoreType.LOCAL_MEMORY)
        if uri.startswith("fs://") or uri.startswith("local://"):
            return StoreURI(uri, StoreType.LOCAL_FILESYSTEM)
        if uri.startswith("http://"):
            return StoreURI(uri, StoreType.REMOTE_HTTP)
        raise RuntimeError(f"Unrecognized backend URI: {uri}.")


# -----------------------------------------------------------------------------
# StoreSession
# -----------------------------------------------------------------------------


class StoreSession:
    """The base class for all implementations of the MLTE store session."""

    def __init__(self):
        """Initialize a session instance."""
        pass

    def close(self) -> None:
        """Close the session."""
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

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
            "Cannot invoke method on abstract StoreSession."
        )

    def read_namespace(self, namespace_id: str) -> Namespace:
        """
        Read a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        :return: The namespace model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def list_namespaces(self) -> list[str]:
        """
        List all MLTE namespaces.
        :return: A collection of identifiers for all MLTE namespaces
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_namespace(self, namespace_id: str) -> Namespace:
        """
        Delete a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        :return: The deleted namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_model(self, namespace_id: str, model: ModelCreate) -> Model:
        """
        Create a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model: The model create model
        :return: The created model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def read_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Read a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :return: The model model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def list_models(self, namespace_id: str) -> list[str]:
        """
        List all MLTE models in the given namespace.
        :param namespace_id: The identifier for the namespace
        :return: A collection of identifiers for all MLTE models
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_model(self, namespace_id: str, model_id: str) -> Model:
        """
        Delete a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :return: The deleted model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
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
            "Cannot invoke method on abstract StoreSession."
        )

    def list_versions(self, namespace_id: str, model_id: str) -> list[str]:
        """
        List all MLTE versions in the given namespace and model.
        :param namespace_id: the identifier for the namespace
        :param model_id: The identifier for the model
        :return: A collection of identifiers for all MLTE versions
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
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
            "Cannot invoke method on abstract StoreSession."
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
            "Cannot invoke method on abstract StoreSession."
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
    ) -> ArtifactModel:
        """
        Write an artifact.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The artifact
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
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
            "Cannot invoke method on abstract StoreSession."
        )

    def read_artifacts(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        filter: ArtifactFilter = AllFilter(),
    ) -> list[ArtifactModel]:
        """
        Read a collection of artifacts, optionally filtered.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param filter: The artifact filter to apply
        :return: A collection of artifacts that satisfy the filter
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
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
            "Cannot invoke method on abstract StoreSession."
        )


# -----------------------------------------------------------------------------
# Store
# -----------------------------------------------------------------------------


class Store:
    """
    An abstract

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def __init__(self, *, uri: StoreURI):
        """
        Initialize a Store instance.
        :param uri: The parsed store URI
        """

        self.uri = uri
        """The parsed artifact store URI."""

    def session(self) -> StoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")


class ManagedSession:
    """A simple context manager for store sessions."""

    def __init__(self, session: StoreSession) -> None:
        self.session = session
        """The wrapped session."""

    def __enter__(self) -> StoreSession:
        return self.session

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.session.close()
