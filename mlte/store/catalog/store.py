"""
mlte/store/catalog/store.py

MLTE catalog store interface implementation.
"""

from __future__ import annotations

import time
import typing

from mlte.catalog.model import CatalogEntry
from mlte.store.base import (
    ManagedSession,
    ResourceMapper,
    Store,
    StoreSession,
    StoreURI,
)
from mlte.store.common.storage import Storage


class CatalogStore(Store):
    read_only: bool = False
    """Whether this catalog is read only or not."""

    def session(self) -> CatalogStoreSession:
        """Return a session handle for a catalog store session instance."""
        raise NotImplementedError("Can't call session on a base Store.")


class CatalogStoreSession(StoreSession):
    """The base class for all implementations of the MLTE catalog store session."""

    entry_mapper: CatalogEntryMapper
    """Mapper for the entry resource."""

    read_only: bool = False
    """Whether this session is read only or not."""

    storage: Storage
    """The underlying storage method."""

    def get_uri(self) -> StoreURI:
        """Returns the URI of the store."""
        return self.storage.get_uri()


class ManagedCatalogSession(ManagedSession):
    """A simple context manager for store sessions."""

    def __enter__(self) -> CatalogStoreSession:
        return typing.cast(CatalogStoreSession, self.session)


class CatalogEntryMapper(ResourceMapper):
    """A interface for mapping CRUD actions to store entries."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def read(self, entry_id: str) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def list(self) -> typing.List[str]:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def delete(self, entry_id: str) -> CatalogEntry:
        raise NotImplementedError(self.NOT_IMPLEMENTED_ERROR_MSG)

    def create_with_header(
        self, entry: CatalogEntry, user: typing.Optional[str] = None
    ) -> CatalogEntry:
        """Create an entry, generating the timestamp and adding creator. Internally calls the appropriate create implementation."""
        entry.header.created = int(time.time())
        entry.header.creator = user
        return self.create(entry)

    def edit_with_header(
        self, entry: CatalogEntry, user: typing.Optional[str] = None
    ) -> CatalogEntry:
        """Edit an entry, generating the proper timestamp. Internally calls the appropriate create implementation."""
        entry.header.updated = int(time.time())
        entry.header.updater = user
        return self.edit(entry)
