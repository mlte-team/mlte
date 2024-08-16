"""
mlte/store/base.py

MLTE general store interface.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, List

from mlte.store.common.query import Query

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
# Store
# -----------------------------------------------------------------------------


class Store:
    """
    An abstract store. A Store instance is the "static" part of a store configuration.
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


# -----------------------------------------------------------------------------
# StoreSession
# -----------------------------------------------------------------------------


class StoreSession:
    """The base class for all implementations of the MLTE store session."""

    resource_mappers: List[ResourceMapper] = []
    """A list of resource mappers for all resources in this store."""

    def __init__(self):
        """Initialize a session instance."""
        pass

    def close(self) -> None:
        """Close the session."""
        raise NotImplementedError(
            "Cannot invoke method on abstract StoreSession."
        )


class ManagedSession:
    """A simple context manager for store sessions."""

    def __init__(self, session: StoreSession) -> None:
        self.session = session
        """The wrapped session."""

    def __enter__(self) -> StoreSession:
        return self.session

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.session.close()


class ResourceMapper:
    """A generic interface for mapping CRUD actions to store specific resources."""

    NOT_IMPLEMENTED_ERROR_MSG = (
        "Cannot invoke method that has not been implemented for this mapper."
    )
    """Default error message for this abstract class."""

    DEFAULT_LIST_LIMIT = 100
    """Default limit for lists."""

    def create(self, new_resource: Any) -> Any:
        """
        Create a new resource.
        :param new_resource: The data to create the resource
        :return: The created resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, updated_resource: Any) -> Any:
        """
        Edit an existing resource.
        :param updated_resource: The data to edit the resource
        :return: The edited resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, resource_identifier: str) -> Any:
        """
        Read a resource.
        :param resource_identifier: The identifier for the resource
        :return: The resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        """
        List all resources of this type in the store.
        :return: A collection of identifiers for all resources of this type
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, resource_identifier: str) -> Any:
        """
        Delete a resource.
        :param resource_identifier: The identifier for the resource
        :return: The deleted resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list_details(
        self,
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[Any]:
        """
        Read details of resources within limit and offset.
        :param limit: The limit on resources to read
        :param offset: The offset on resources to read
        :return: The read resources
        """
        entry_ids = self.list()
        return [self.read(entry_id) for entry_id in entry_ids][
            offset : offset + limit
        ]

    def search(
        self,
        query: Query = Query(),
    ) -> List[Any]:
        """
        Read a collection of resources, optionally filtered.
        :param query: The resource query to apply
        :return: A collection of resources that satisfy the filter
        """
        # TODO: not the most efficient way, since it loads all items first, before filtering.
        entries = self.list_details()
        return [entry for entry in entries if query.filter.match(entry)]
