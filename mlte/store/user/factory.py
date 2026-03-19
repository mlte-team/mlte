"""Top-level functions for artifact store creation."""

from mlte.store.base import StoreType, StoreURI
from mlte.store.user.store import UserStore
from mlte.store.user.underlying.fs import FileSystemUserStore
from mlte.store.user.underlying.http import HttpUserStore
from mlte.store.user.underlying.memory import InMemoryUserStore


def create_user_store(parsed_uri: StoreURI) -> UserStore:
    """
    Create a MLTE user store instance.
    :param parsed_uri: The URI for the store instance
    :return: The store instance
    """
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryUserStore(parsed_uri)
    if parsed_uri.type == StoreType.RELATIONAL_DB:
        # Import is here to avoid importing SQL libraries if they have not been installed.
        from mlte.store.user.underlying.rdbs.store import RelationalDBUserStore

        return RelationalDBUserStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemUserStore(parsed_uri)
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        return HttpUserStore(uri=parsed_uri)
    else:
        raise Exception(
            f"User store can't be created, unknown or unsupported URI type received for uri {parsed_uri}"
        )
