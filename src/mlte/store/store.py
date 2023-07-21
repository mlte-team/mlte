"""
mlte/store/backend/store.py

MLTE artifact store interface implementation.
"""

from __future__ import annotations

from enum import Enum
from collections.abc import Generator

from mlte.context.model import (
    Namespace,
    Model,
    Version,
)
from mlte.negotiation.model import NegotiationCardModel

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

    def create_namespace(self, namespace: Namespace) -> None:
        """
        Create a MLTE namespace.
        :param namespace: The namespace model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def read_namespace(self, namespace_id: str) -> list[Model]:
        """
        Read a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        :return: A collection of the models in the namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_namespace(self, namespace_id: str) -> None:
        """
        Delete a MLTE namespace.
        :param namespace_id: The identifier for the namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_model(self, namespace_id: str, model: Model) -> None:
        """
        Create a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model: The model model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def read_model(self, namespace_id: str, model_id: str) -> list[Version]:
        """
        Read a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :return: A collection of the versions in the namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_model(self, namespace_id: str, model_id: str) -> None:
        """
        Delete a MLTE model.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_version(
        self, namespace_id: str, model_id: str, version: Version
    ) -> None:
        """
        Create a MLTE model version.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version: The version
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
        """
        # TODO(Kyle): What should this operation represent?
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_version(
        self, namespace_id: str, model_id: str, version_id: str
    ) -> None:
        """
        Delete a MLTE model version.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact: NegotiationCardModel,
    ) -> None:
        """
        Create a negotiation card artifact.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact: The negotiation card artifact
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def read_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> NegotiationCardModel:
        """
        Read a negotiation card artifact.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact_id: The artifact identifier
        :return: The artifact
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_negotiation_card(
        self,
        namespace_id: str,
        model_id: str,
        version_id: str,
        artifact_id: str,
    ) -> None:
        """
        Delete a negotiation card artifact.
        :param namespace_id: The identifier for the namespace
        :param model_id: The identifier for the model
        :param version_id: The identifier for the model version
        :param artifact_id: The artifact identifier
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

    def session(self) -> Generator[StoreSession, None, None]:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")