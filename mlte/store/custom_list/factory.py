"""Top-level functions for custom list store creation."""

from mlte.store.base import StoreType, StoreURI
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.underlying.fs import FileSystemCustomListStore
from mlte.store.custom_list.underlying.memory import InMemoryCustomListStore

# from mlte.store.custom_list.underlying.rdbs.store import RelationalDBCustomListStore
# from mlte.store.custom_list.underlying.rdbs.store import HttpCustomListStore


def create_custom_list_store(uri: str) -> CustomListStore:
    """
    Create a MLTE custom list store instance.
    :param uri: The URI for the store instance
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)

    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryCustomListStore(parsed_uri)
    #   elif parsed_uri.type == StoreType.RELATIONAL_DB:
    # return RelationalDBCustomListStore(parsed_uri)
    elif parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemCustomListStore(parsed_uri)
    #   elif parsed_uri.type == StoreType.REMOTE_HTTP:
    # return HttpCustomListStore(uri=parsed_uri)
    else:
        raise Exception(
            f"Store can't be created, unknown or unsupported URI prefix received for uri {parsed_uri}"
        )
