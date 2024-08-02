"""
mlte/store/catalog/factory.py

Top-level functions for catalog store creation.
"""

from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore


def create_store(uri: str) -> CatalogStore:
    """
    Create a MLTE catalog store instance.
    :param uri: The URI for the store instance
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryCatalogStore(parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemCatalogStore(parsed_uri)

    raise Exception(f"Invalid store type: {uri}")
