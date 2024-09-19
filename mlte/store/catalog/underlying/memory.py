"""
mlte/store/catalog/underlying/memory.py

Implementation of in-memory catalog store.
"""

from __future__ import annotations

from typing import Dict, List

import mlte.store.error as errors
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.common.storage import Storage

# -----------------------------------------------------------------------------
# Memory Store
# -----------------------------------------------------------------------------


class InMemoryCatalogStore(CatalogStore):
    """An in-memory implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI) -> None:
        self.storage = MemoryCatalogStorage(uri)
        """The underlying storage for the store."""

        super().__init__(uri=uri)
        """Store uri."""

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return InMemoryCatalogStoreSession(
            storage=self.storage, read_only=self.read_only
        )

    def clone(self) -> InMemoryCatalogStore:
        """
        Clones the store. Shallow clone.
        :return: The cloned store
        """
        clone = InMemoryCatalogStore(self.uri)
        clone.storage.entries = self.storage.entries.copy()
        return clone


class MemoryCatalogStorage(Storage):
    """A simple storage wrapper for the in-memory store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri)

        self.entries: Dict[str, CatalogEntry] = {}


# -----------------------------------------------------------------------------
# InMemoryCatalogStoreSession
# -----------------------------------------------------------------------------


class InMemoryCatalogStoreSession(CatalogStoreSession):
    """An in-memory implementation of the MLTE user store."""

    def __init__(
        self, *, storage: MemoryCatalogStorage, read_only: bool = False
    ) -> None:
        self.storage = storage
        """The storage."""

        self.read_only = read_only
        """Whether this is read only or not."""

        self.entry_mapper = InMemoryCatalogEntryMapper(storage=storage)

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass


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
