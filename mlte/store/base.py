"""
mlte/store/base.py

MLTE general store interface.
"""

from __future__ import annotations

from enum import Enum

# -----------------------------------------------------------------------------
# StoreType
# -----------------------------------------------------------------------------


class StoreType(Enum):
    """Represents the type of an MLTE store."""

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
    """Represents the URI for an store instance."""

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


# -----------------------------------------------------------------------------
# Store
# -----------------------------------------------------------------------------


class Store:
    """
    An abstract store.

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def __init__(self, *, uri: StoreURI):
        """
        Initialize a Store instance.
        :param uri: The parsed store URI
        """

        self.uri = uri
        """The parsed store URI."""

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
