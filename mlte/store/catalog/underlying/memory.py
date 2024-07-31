"""
mlte/store/catalog/underlying/memory.py

Implementation of in-memory catalog store.
"""

from __future__ import annotations

from typing import Dict, List

from mlte.store.common.query import Query
import mlte.store.error as errors
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)

# -----------------------------------------------------------------------------
# Memory Store
# -----------------------------------------------------------------------------


class InMemoryCatalogStore(CatalogStore):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI) -> None:
        self.storage = MemoryCatalogStorage()
        """The underlying storage for the store."""

        # Initialize defaults.
        super().__init__(uri=uri)

    def session(self) -> InMemoryCatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryCatalogStoreSession(storage=self.storage)

    def clone(self) -> InMemoryCatalogStore:
        """
        Clones the store. Shallow clone.
        :return: The cloned store
        """
        clone = InMemoryCatalogStore(self.uri)
        clone.storage.entries = self.storage.entries.copy()
        return clone


class MemoryCatalogStorage:
    """A simple storage wrapper for the in-memory store."""

    def __init__(self) -> None:
        self.entries: Dict[str, CatalogEntry] = {}


# -----------------------------------------------------------------------------
# InMemoryCatalogStoreSession
# -----------------------------------------------------------------------------


class InMemoryCatalogStoreSession(CatalogStoreSession):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, *, storage: MemoryCatalogStorage) -> None:
        self.storage = storage
        """The storage."""

        self.entry_mapper = InMemoryCatalogEntryMapper(storage=storage)

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass

    def read_entries(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        return [entry for entry in self.storage.entries.values()][
            offset : offset + limit
        ]

    def search_entries(
        self,
        query: Query = Query(),
    ) -> List[CatalogEntry]:
        return [
            entry
            for entry in self.storage.entries.values()
            if query.filter.match(entry)
        ]


class InMemoryCatalogEntryMapper(CatalogEntryMapper):
    """In-memory mapper for the catalog resource."""

    def __init__(self, *, storage: MemoryCatalogStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        if entry.header.identifier in self.storage.entries:
            raise errors.ErrorAlreadyExists(f"Entry {entry.header.identifier}")

        self.storage.entries[entry.header.identifier] = entry
        return entry

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        if entry.header.identifier not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {entry.header.identifier}")

        self.storage.entries[entry.header.identifier] = entry
        return entry

    def read(self, entry_id: str) -> CatalogEntry:
        if entry_id not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {entry_id}")

        entry = self.storage.entries[entry_id]
        return entry

    def list(self) -> List[str]:
        return [username for username in self.storage.entries.keys()]

    def delete(self, entry_id: str) -> CatalogEntry:
        if entry_id not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {entry_id}")

        popped = self.storage.entries[entry_id]
        del self.storage.entries[entry_id]
        return popped
