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

    RELATIONAL_DB = "relational_db"
    """A relational database system implementation."""


# -----------------------------------------------------------------------------
# StoreURIPrefix
# -----------------------------------------------------------------------------


class StoreURIPrefix:
    """Represents the valid prefixes for a MLTE store URI."""

    LOCAL_MEMORY = ["memory://"]
    """The in-memory store prefix."""

    LOCAL_FILESYSTEM = ["fs://", "local://"]
    """The local filesystem prefixes."""

    REMOTE_HTTP = ["http://"]
    """The remote HTTP prefix."""

    RELATIONAL_DB = ["sqlite", "mysql", "postgresql", "oracle", "mssql"]
    """The relational database system prefixes."""


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
        if uri.startswith(tuple(StoreURIPrefix.LOCAL_MEMORY)):
            return StoreURI(uri, StoreType.LOCAL_MEMORY)
        if uri.startswith(tuple(StoreURIPrefix.LOCAL_FILESYSTEM)):
            return StoreURI(uri, StoreType.LOCAL_FILESYSTEM)
        if uri.startswith(tuple(StoreURIPrefix.REMOTE_HTTP)):
            return StoreURI(uri, StoreType.REMOTE_HTTP)
        if uri.startswith(tuple(StoreURIPrefix.RELATIONAL_DB)):
            return StoreURI(uri, StoreType.RELATIONAL_DB)
        raise RuntimeError(f"Unrecognized backend URI: {uri}.")

    def __str__(self) -> str:
        return f"{self.type}:{self.uri}"


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
