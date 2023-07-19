"""
mlte/store/backend/store.py

MLTE artifact store interface implementation.
"""

from __future__ import annotations

from enum import Enum

from mlte.context.model import (
    NamespaceModel,
    ModelIdentifierModel,
    ModelVersionModel,
)

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

    def __enter__(self) -> None:
        """StoreSession implements a context manager."""
        return self

    def __exit__(self) -> None:
        """StoreSession implements a context manager."""
        self.close()

    def close(self) -> None:
        """Close the session."""
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_namespace(namespace: NamespaceModel) -> None:
        """
        Create a MLTE namespace.
        :param namespace: The namespace model
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def read_namespace(id: str) -> list[ModelIdentifierModel]:
        """
        Read a MLTE namespace.
        :param id: The identifier for the namespace
        :return: A collection of the models in the namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def delete_namespace(id: str) -> None:
        """
        Delete a MLTE namespace.
        :param id: The identifier for the namespace
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )

    def create_model(namespace_id: str, model: ModelIdentifierModel) -> None:
        pass

    def read_model(namespace_id: str, model_id: str) -> list[ModelVersionModel]:
        pass


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
