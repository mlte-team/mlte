"""
Backend initialization.
"""

from typing import Any, Dict, Optional

from .backend import Backend, BackendURI, BackendType
from .fs import FilesystemBackendBuilder


def _parse_uri(uri: str) -> BackendURI:
    """
    Parse the URI for a backend store.
    :param uri: The URI for the backend store
    :type uri: str
    :return: The parsed BackendStoreURI
    :rtype: BackendStoreURI
    """
    return BackendURI.from_string(uri)


def initialize_backend(
    uri: str, environment: Optional[Dict[str, Any]] = None
) -> Backend:
    """
    Prepare the backend store for use.
    :param uri: The URI for the backend store
    :type uri: str
    :param environment: The environment used to initialize the store
    :type: environment: Optional[Dict[str, Any]]
    :return: The prepared backend store
    :rtype: BackendStore
    """
    parsed = _parse_uri(uri)
    if parsed.type == BackendType.FS:
        return FilesystemBackendBuilder().with_uri(parsed).build()  # type: ignore
    raise RuntimeError(f"Unknown URI type: {parsed}.")
