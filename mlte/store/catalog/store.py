"""
mlte/store/catalog/store.py

MLTE catalog store interface implementation.
"""

from __future__ import annotations

from typing import List, cast

from mlte.catalog.model import CatalogEntryModel
from mlte.store.base import ManagedSession, Store, StoreSession


class CatalogStore(Store):
    """
    An abstract store.

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")


class CatalogStoreSession(StoreSession):
    """The base class for all implementations of the MLTE catalog store session."""

    def write_entry(
        self,
        catalog_id: str,
        entry: CatalogEntryModel,
        *,
        force: bool = False,
    ) -> CatalogEntryModel:
        """
        Write an catalog entry.
        :param catalog_id: The identifier of the catalog to store this to.
        :param entry: The catalog entry
        :param force: Overwrite an entry if it already exists
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract CatalogStoreSession."
        )

    def read_entry(
        self,
        entry_id: str,
    ) -> CatalogEntryModel:
        """
        Read a catalog entry.
        :param catalog_id: The identifier of the catalog to read from.
        :param entry_id: The catalog entry identifier
        :return: The entry
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract CatalogStoreSession."
        )

    def read_entries(
        self,
        catalog_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CatalogEntryModel]:
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
    ) -> List[CatalogEntryModel]:
        """
         Read a collection of entries, optionally filtered.
         :param catalog_id: The identifier of the catalog to read from.
        # :param query: The entry query to apply
         :return: A collection of entries that satisfy the filter
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract CatalogStoreSession."
        )

    def delete_entry(
        self,
        catalog_id: str,
        entry_id: str,
    ) -> CatalogEntryModel:
        """
        Delete an entry.
        :param catalog_id: The identifier of the catalog to delete this from.
        :param entry_id: The catalog entry identifier
        :return: The deleted entry
        """
        raise NotImplementedError(
            "Cannot invoke method on abstract ArtifactStoreSession."
        )


class ManagedCatalogSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> CatalogStoreSession:
        return cast(CatalogStoreSession, self.session)
