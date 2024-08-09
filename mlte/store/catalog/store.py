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
