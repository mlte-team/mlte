"""
mlte/store/factory.py

Top-level functions for artifact store creation.
"""

from mlte.store.underlying.memory import InMemoryStore
from mlte.store.store import Store, StoreURI, StoreType


def create_store(uri: str) -> Store:
    """
    Create a MLTE artifact store instance.
    :param uri: The URI for the store instance
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        raise NotImplementedError("Not implemented.")
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        raise NotImplementedError("Not implemented.")
    assert False, "Unreachable."