"""
mlte/store/catalog/store.py

MLTE catalog store interface implementation.
"""

from __future__ import annotations

from typing import List, cast

from mlte.catalog.model import CatalogEntry
from mlte.store.base import ManagedSession, ResourceMapper, Store, StoreSession


class CatalogStore(Store):
    """
    An abstract store.
    """

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")


class CatalogStoreSession(StoreSession):
    """The base class for all implementations of the MLTE catalog store session."""

    def __init__(self):
        self.entry_mapper = CatalogEntryMapper()
        """Mapper for the entry resource."""

    def read_entries(
        self,
        catalog_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        """
        Read entries within limit and offset.
        :param catalog_id: The identifier of the catalog to read from.
        :param limit: The limit on entries to read
        :param offset: The offset on entries to read
        :return: The read entries
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract CatalogStoreSession."
        )

    def search_entries(
        self,
        catalog_id: str,
        # query: Query = Query(),
    ) -> List[CatalogEntry]:
        """
         Read a collection of entries, optionally filtered.
         :param catalog_id: The identifier of the catalog to read from.
        # :param query: The entry query to apply
         :return: A collection of entries that satisfy the filter
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract CatalogStoreSession."
        )


class CatalogEntryMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store entries."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, entry_id: str) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, entry_id: str) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)


class ManagedCatalogSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> CatalogStoreSession:
        return cast(CatalogStoreSession, self.session)
