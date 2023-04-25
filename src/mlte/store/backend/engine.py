"""
store/backend/engine.py

Backend engine creation. This is the first
step in the backend initialization lifecycle.
"""

from mlte.store.backend import BackendEngine, BackendURI, BackendType
from mlte.store.backend.fs import FilesystemBackendEngine


def _parse_uri(uri: str) -> BackendURI:
    """
    Parse the URI for a backend store.
    :param uri: The URI for the backend store
    :type uri: str
    :return: The parsed BackendStoreURI
    :rtype: BackendStoreURI
    """
    return BackendURI.from_string(uri)


def create_engine(uri: str) -> BackendEngine:
    """
    Create the backend engine.
    :param uri: The URI string
    :type uri: str
    :return: The engine
    :rtype: BackendEngine
    """
    parsed_uri = _parse_uri(uri)
    if parsed_uri.type == BackendType.FS:
        return FilesystemBackendEngine.create(parsed_uri)
    raise RuntimeError(f"Unknown URI type: {parsed_uri}.")
