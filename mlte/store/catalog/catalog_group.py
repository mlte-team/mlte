"""
mlte/store/catalog/catalog_group.py

MLTE catalog store group interface implementation.
"""

from __future__ import annotations

import typing
from typing import Dict, List, Optional, cast

from mlte.catalog.model import CatalogEntry
from mlte.store.base import ManagedSession, StoreSession
from mlte.store.catalog.factory import create_catalog_store
from mlte.store.catalog.store import CatalogStore, CatalogStoreSession
from mlte.store.error import ErrorAlreadyExists, ErrorNotFound
from mlte.store.query import Query


class CatalogStoreGroup:
    """
    A group of catalog stores.
    """

    def __init__(self):
        """Initialization."""
        self.catalogs: Dict[str, CatalogStore] = {}
        """Dictionary with all catalogs in this group."""

    def add_catalog_from_uri(self, id: str, uri: str, overwrite: bool = False):
        """
        Adds a catalog by indicating its uri.

        :param id: A string to identify the catalog.
        :param uri: The store URI that describes the store to be used for the catalog.
        :param overwrite: Add catalog to list even if id is already stored, pointing dictionary id to the new URI.
        """
        catalog = create_catalog_store(uri, id)
        self.add_catalog(id, catalog, overwrite)

    def add_catalog(
        self, id: str, catalog_store: CatalogStore, overwrite: bool = False
    ):
        """
        Adds a catalog.

        :param id: A string to identify the catalog.
        :param catalog_store: The catalog store to add.
        :param overwrite: Add catalog to list even if id is already stored, pointing dictionary id to the new URI.
        """
        if id in self.catalogs and not overwrite:
            raise ErrorAlreadyExists(
                f"Catalog with id {id} already exists in group."
            )
        self.catalogs[id] = catalog_store

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


class CatalogStoreGroupSession(StoreSession):
    """Sessions for all catalogs in a group."""

    def __init__(self, catalogs: Dict[str, CatalogStore]):
        """Initialize a session instance for each catalog."""
        self.sessions: Dict[str, CatalogStoreSession] = {}
        """Sessions for all catalogs in the group."""

        for id, catalog in catalogs.items():
            self.sessions[id] = catalog.session()

    def close(self) -> None:
        """Close all sessions."""
        for _, session in self.sessions.items():
            session.close()

    def get_session(self, catalog_id: str) -> CatalogStoreSession:
        """Gets a session for the given catalog store id."""
        if catalog_id not in self.sessions:
            raise ErrorNotFound(
                f"Catalog id {catalog_id} was not found in registered list of catalogs -"
            )
        return self.sessions[catalog_id]

    def list_details(
        self,
        catalog_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        """
        Read entries within limit and offset.
        :param catalog_id: The identifier of the catalog to read from; if not given, read from all catalogs.
        :param limit: The limit on entries to read
        :param offset: The offset on entries to read
        :return: The read entries
        """
        if catalog_id is not None:
            if catalog_id not in self.sessions:
                raise ErrorNotFound(
                    f"Catalog id {catalog_id} was not found in list of catalogs."
                )

            catalog_session = self.sessions[catalog_id]
            return catalog_session.entry_mapper.list_details(limit, offset)
        else:
            # Go over all catalogs, reading from each one, and grouping results.
            results: List[CatalogEntry] = []
            for catalog_id, session in self.sessions.items():
                partial_results = session.entry_mapper.list_details(
                    limit, offset
                )
                results.extend(partial_results)
            return results[offset : offset + limit]

    def search(
        self,
        catalog_id: Optional[str] = None,
        query: Query = Query(),
    ) -> List[CatalogEntry]:
        """
        Read a collection of entries, optionally filtered.
        :param catalog_id: The identifier of the catalog to read from; if not given, search on all catalogs.
        :param query: The entry query to apply
        :return: A collection of entries that satisfy the filter
        """
        if catalog_id is not None:
            if catalog_id not in self.sessions:
                raise ErrorNotFound(
                    f"Catalog id {catalog_id} was not found in list of catalogs."
                )

            catalog_session = self.sessions[catalog_id]
            entries = typing.cast(
                List[CatalogEntry], catalog_session.entry_mapper.search(query)
            )

            # Ensure they are marked as coming from this catalog.
            for entry in entries:
                entry.header.catalog_id = catalog_id
            return entries
        else:
            # Go over all catalogs, reading from each one, and grouping results.
            results: List[CatalogEntry] = []
            for catalog_id, session in self.sessions.items():
                # Get results for this catalog.
                partial_results = typing.cast(
                    List[CatalogEntry], session.entry_mapper.search(query)
                )

                # Ensure they are marked as coming from this catalog.
                for entry in partial_results:
                    entry.header.catalog_id = catalog_id

                # Add them to the overall lilst.
                results.extend(partial_results)
            return results


class ManagedCatalogGroupSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> CatalogStoreGroupSession:
        return cast(CatalogStoreGroupSession, self.session)
