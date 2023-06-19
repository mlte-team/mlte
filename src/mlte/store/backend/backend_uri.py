"""
mlte/store/backend/backend_uri.py

Definitions for backend URI types.
"""

from __future__ import annotations

from enum import Enum

# -----------------------------------------------------------------------------
# BackendType
# -----------------------------------------------------------------------------


class BackendType(Enum):
    """Represents the type of backend store."""

    # Use the local filesystem as the backend store
    FS = 0


# -----------------------------------------------------------------------------
# BackendURI
# -----------------------------------------------------------------------------


class BackendURI:
    """Represents the URI for a backend store."""

    def __init__(self, uri: str, type: BackendType):
        """
        Initialize a BackendURI instance.
        :param uri: The URI
        :type uri: str
        :param type: The type of the backend store
        :type type: StoreType
        """
        self.uri = uri
        """The string that represents the URI."""

        self.type = type
        """The type identifier for the URI."""

    @staticmethod
    def from_string(uri: str) -> BackendURI:
        """
        Parse a BackendURI from a string.
        :param uri: The URI
        :type uri: str
        :return: The parsed BackendURI
        :rtype: BackendURI
        """
        if uri.startswith("fs://") or uri.startswith("local://"):
            return BackendURI(uri, BackendType.FS)
        raise RuntimeError(f"Unrecognized backend URI: {uri}.")
