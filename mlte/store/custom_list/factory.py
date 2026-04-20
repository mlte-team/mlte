"""Top-level functions for custom list store creation."""

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.http import HttpCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore


def create_custom_list_store(parsed_uri: StoreURI) -> CustomListStore:
    """
    Create a MLTE custom list store instance.
    :param parsed_uri: The URI for the store instance
    :return: The store instance
    """
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        return HttpCustomListStore(uri=parsed_uri)
    elif parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryCustomListStore(parsed_uri)
    elif parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemCustomListStore(parsed_uri)
    elif parsed_uri.type == StoreType.RELATIONAL_DB:
        # Import is here to avoid importing SQL libraries if they have not been installed.
        from mlte.store.custom_list.underlying.rdbs.store import (
            RDBCustomListStore,
        )

        return RDBCustomListStore(parsed_uri)
    else:
        raise Exception(
            f"Custom list store can't be created, unknown or unsupported URI type received for uri {parsed_uri}"
        )
