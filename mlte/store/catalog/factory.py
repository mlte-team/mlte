"""
mlte/store/catalog/factory.py

Top-level functions for catalog store creation.
"""


from typing import Optional

from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.fs import FileSystemCatalogStore
from mlte.store.catalog.underlying.http import HttpCatalogGroupStore
from mlte.store.catalog.underlying.memory import InMemoryCatalogStore
from mlte.store.catalog.underlying.rdbs.store import RelationalDBCatalogStore


def create_catalog_store(
    uri: str, catalog_id: Optional[str] = None
) -> CatalogStore:
    """
    Create a MLTE catalog store instance.
    :param uri: The URI for the store instance
    :param catalog_id: The id used to identify the catalog.
    :return: The store instance
    """
    parsed_uri = StoreURI.from_string(uri)
    if parsed_uri.type == StoreType.LOCAL_MEMORY:
        return InMemoryCatalogStore(uri=parsed_uri)
    if parsed_uri.type == StoreType.LOCAL_FILESYSTEM:
        return FileSystemCatalogStore(uri=parsed_uri, catalog_folder=catalog_id)
    if parsed_uri.type == StoreType.RELATIONAL_DB:
        return RelationalDBCatalogStore(uri=parsed_uri)
    if parsed_uri.type == StoreType.REMOTE_HTTP:
        return HttpCatalogGroupStore(uri=parsed_uri)

    raise Exception(f"Invalid store type: {uri}")
