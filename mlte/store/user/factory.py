"""
mlte/store/artifact/factory.py

Top-level functions for artifact store creation.
"""

from mlte.store.base import StoreType, StoreURI
from mlte.store.user.store import UserStore
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore
from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore


def create_user_store(uri: str) -> UserStore:
    """
    Create a MLTE user store instance.
    :param uri: The URI for the store instance
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryUserStore(parsed_uri)
    if parsed_uri.type == StoreType.RELATIONAL_DB:
        return RelationalDBUserStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemUserStore(parsed_uri)
    else:
        raise Exception(
            f"Store can't be created, unknown or unsupported URI prefix received for uri {parsed_uri}"
        )
