"""
mlte/store/base.py

MLTE general store interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, List, Optional, Protocol

from mlte.store.query import Query

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

    RELATIONAL_DB = "database"
    """A relational database system implementation."""


# -----------------------------------------------------------------------------
# StoreURI
# -----------------------------------------------------------------------------


class StoreURI:
    """Represents the URI for an store instance."""

    PREFIXES = {
        StoreType.LOCAL_MEMORY: ["memory"],
        StoreType.LOCAL_FILESYSTEM: ["fs", "local"],
        StoreType.REMOTE_HTTP: ["http"],
        StoreType.RELATIONAL_DB: [
            "sqlite",
            "mysql",
            "postgresql",
            "oracle",
            "mssql",
        ],
    }
    """Valid prefixes by store type."""

    DELIMITER = "://"
    """Delimiter used to separate prefixes from rest of the path."""

    DEFAULT_STORES_FOLDER = "default_store"
    """Default root folder for all built-in file-based stores."""

    def __init__(self, uri: str, type: StoreType, path: str, prefix: str):
        """
        Initialize a StoreURI instance.
        :param uri: The URI
        :param type: The type of the backend store
        :param path: The rest of the URI's path with the prefix removed
        """
        self.uri = uri
        """The string that represents the URI."""

        self.type = type
        """The type identifier for the URI."""

        self.path = path
        """The rest of the path, with the prefix removed."""

        self.prefix = prefix
        """The actual prefix used in the type."""

    @staticmethod
    def from_string(uri: str) -> StoreURI:
        """
        Parse a StoreURI from a string.
        :param uri: The URI
        :return: The parsed StoreURI
        """
        prefix, path = StoreURI._parse_uri(uri)

        try:
            type = StoreURI.get_type(prefix)
            return StoreURI(uri, type, path, prefix)
        except Exception as e:
            # If we got here, the stucture of the URI is fine, but the prefix is unknown.
            raise RuntimeError(f"Unsupported store URI: {uri}") from e

    @staticmethod
    def get_type(prefix: str) -> StoreType:
        """Returns the type given a prefix."""
        for type in StoreType:
            if prefix.startswith(tuple(StoreURI.PREFIXES[type])):
                return type
        raise RuntimeError(
            f"Prefix {prefix} is not associated to any known type."
        )

    @staticmethod
    def _parse_uri(uri: str) -> tuple[str, str]:
        """Split an URI into its prefix and the rest of the path."""
        parts = uri.split(StoreURI.DELIMITER)
        if len(parts) != 2:
            raise RuntimeError(f"Invalid store URI: {uri}")
        else:
            prefix = parts[0]
            path = parts[1]
            return prefix, path

    @staticmethod
    def create_uri_string(type: StoreType, path: Optional[str] = None) -> str:
        """Creates a URI using the default (first) prefix for the given type."""
        prefix = StoreURI.PREFIXES[type][0]
        return f"{prefix}{StoreURI.DELIMITER}{path}"

    @staticmethod
    def create_default_fs_uri() -> StoreURI:
        """Creates the default StoreURI for file system stores."""
        uri_string = StoreURI.create_uri_string(
            type=StoreType.LOCAL_FILESYSTEM,
            path=StoreURI.DEFAULT_STORES_FOLDER,
        )
        return StoreURI.from_string(uri_string)

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
        raise NotImplementedError("Can't call session on a base Store.")


# -----------------------------------------------------------------------------
# StoreSession
# -----------------------------------------------------------------------------


class StoreSession(Protocol):
    """The base class for all implementations of the MLTE store session."""

    def close(self) -> None:
        """Close the session."""
        ...


class ManagedSession:
    """A simple context manager for store sessions."""

    def __init__(self, session: StoreSession) -> None:
        self.session = session
        """The wrapped session."""

    def __enter__(self) -> StoreSession:
        return self.session

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.session.close()


class ResourceMapper(ABC):
    """
    A generic interface for mapping CRUD actions to store specific resources.
    """

    NOT_IMPLEMENTED_ERROR_MSG = (
        "Cannot invoke method that has not been implemented for this mapper."
    )
    """Default error message for this abstract class."""

    DEFAULT_LIST_LIMIT = 100
    """Default limit for lists."""

    @abstractmethod
    def create(self, new_resource: Any, context: Any = None) -> Any:
        """
        Create a new resource.
        :param new_resource: The data to create the resource
        :param context: Any additional context needed for this resource.
        :return: The created resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def edit(self, updated_resource: Any, context: Any = None) -> Any:
        """
        Edit an existing resource.
        :param updated_resource: The data to edit the resource
        :param context: Any additional context needed for this resource.
        :return: The edited resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def read(self, resource_identifier: str, context: Any = None) -> Any:
        """
        Read a resource.
        :param resource_identifier: The identifier for the resource
        :param context: Any additional context needed for this resource.
        :return: The resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def list(self, context: Any = None) -> List[str]:
        """
        List all resources of this type in the store.
        :param context: Any additional context needed for this resource.
        :return: A collection of identifiers for all resources of this type
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    @abstractmethod
    def delete(self, resource_identifier: str, context: Any = None) -> Any:
        """
        Delete a resource.
        :param resource_identifier: The identifier for the resource
        :param context: Any additional context needed for this resource.
        :return: The deleted resource
        """
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list_details(
        self,
        context: Any = None,
        limit: int = DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[Any]:
        """
        Read details of resources within limit and offset.
        :param context: Any additional context needed for this resource.
        :param limit: The limit on resources to read
        :param offset: The offset on resources to read
        :return: The read resources
        """
        entry_ids = self.list(context)
        return [self.read(entry_id, context) for entry_id in entry_ids][
            offset : offset + limit
        ]

    def search(self, query: Query = Query(), context: Any = None) -> List[Any]:
        """
        Read a collection of resources, optionally filtered.
        :param query: The resource query to apply
        :param context: Any additional context needed for this resource.
        :return: A collection of resources that satisfy the filter
        """
        # TODO: not the most efficient way, since it loads all items first, before filtering.
        entries = self.list_details(context)
        return [entry for entry in entries if query.filter.match(entry)]
