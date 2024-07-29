"""
mlte/store/catalog/group.py

MLTE catalog store group interface implementation.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreSession
from mlte.store.catalog.factory import create_store
from mlte.store.catalog.store import CatalogStore, CatalogStoreSession
from mlte.store.error import ErrorAlreadyExists, ErrorNotFound


class CatalogStoreGroup:
    """
    An group of catalog stores.
    """

    catalogs: Dict[str, CatalogStore] = {}
    """Dictionary with all catalogs in this group."""

    def add_catalog(self, id: str, uri: str, overwite: bool = False):
        """Adds a catalog by indicating its uri."""
        if id in self.catalogs and not overwite:
            raise ErrorAlreadyExists(
                f"Catalog with id {id} already exists in group."
            )

        catalog = create_store(uri)
        self.catalogs[id] = catalog

    def remove_catalog(self, id: str):
        """Removes the given catalog."""
        if id not in self.catalogs:
            raise ErrorNotFound(f"Catalog with id {id} was not found in group.")

        del self.catalogs[id]

    def session(self) -> CatalogStoreGroupSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return CatalogStoreGroupSession(self.catalogs)

    def read_entries(
        self,
        catalog_id: Optional[str] = None,
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
        catalog_id: Optional[str] = None,
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


class CatalogStoreGroupSession(StoreSession):
    """Sessions for all catalogs in a group."""

    sessions: Dict[str, CatalogStoreSession] = {}
    """Sessions for all catalogs in the group."""

    def __init__(self, catalogs: Dict[str, CatalogStore]):
        """Initialize a session instance for each catalog."""
        for id, catalog in catalogs.items():
            self.sessions[id] = catalog.session()

    def close(self) -> None:
        """Close all sessions."""
        for _, session in self.sessions.items():
            session.close()
