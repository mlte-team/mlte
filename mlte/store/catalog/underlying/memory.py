"""Implementation of in-memory catalog store."""

from __future__ import annotations

from typing import Any, Dict, List

import mlte.store.error as errors
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.store_session import (
    CatalogEntryMapper,
    CatalogStoreSession,
)
from mlte.store.common.storage import Storage
from mlte.store.validators.composite_validator import CompositeValidator

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
            storage=self.storage,
            validators=self.validators,
            read_only=self.read_only,
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
        self,
        *,
        storage: MemoryCatalogStorage,
        validators: CompositeValidator,
        read_only: bool = False,
    ) -> None:
        self.storage = storage
        """The storage."""

        self.read_only = read_only
        """Whether this is read only or not."""

        self.entry_mapper = InMemoryCatalogEntryMapper(
            storage=storage, validators=validators
        )

    def close(self) -> None:
        """Close the session."""
        # Closing an in-memory session is a no-op.
        pass


class InMemoryCatalogEntryMapper(CatalogEntryMapper):
    """In-memory mapper for the catalog resource."""

    def __init__(
        self, *, storage: MemoryCatalogStorage, validators: CompositeValidator
    ) -> None:
        super().__init__()

        self.storage = storage
        """A reference to underlying storage."""

        self.validators: CompositeValidator = validators

    def create(
        self, new_entry: CatalogEntry, context: Any = None
    ) -> CatalogEntry:
        self.validators.validate_all(new_entry)
        if new_entry.header.identifier in self.storage.entries:
            raise errors.ErrorAlreadyExists(
                f"Entry {new_entry.header.identifier}"
            )

        self.storage.entries[new_entry.header.identifier] = new_entry
        return new_entry

    def edit(
        self, new_entry: CatalogEntry, context: Any = None
    ) -> CatalogEntry:
        self.validators.validate_all(new_entry)
        if new_entry.header.identifier not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {new_entry.header.identifier}")

        self.storage.entries[new_entry.header.identifier] = new_entry
        return new_entry

    def read(self, entry_id: str, context: Any = None) -> CatalogEntry:
        if entry_id not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {entry_id}")

        entry = self.storage.entries[entry_id]
        return entry

    def list(self, context: Any = None) -> List[str]:
        return [username for username in self.storage.entries.keys()]

    def delete(self, entry_id: str, context: Any = None) -> CatalogEntry:
        if entry_id not in self.storage.entries:
            raise errors.ErrorNotFound(f"Entry {entry_id}")

        popped = self.storage.entries[entry_id]
        del self.storage.entries[entry_id]
        return popped
