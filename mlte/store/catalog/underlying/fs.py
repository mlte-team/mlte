"""
mlte/store/catalog/underlying/fs.py

Implementation of local file system catalog store.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.common.fs import FileSystemStorage
from mlte.store.common.query import Query

# -----------------------------------------------------------------------------
# LocalFileSystemStore
# -----------------------------------------------------------------------------


class FileSystemCatalogStore(CatalogStore):
    """A local file system implementation of the MLTE catalog store."""

    BASE_CATALOG_FOLDER = "catalog"
    """Base fodler to store catalog entries in."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

        self.storage = FileSystemStorage(
            uri=uri, sub_folder=self.BASE_CATALOG_FOLDER
        )
        """The underlying storage for the store."""

    def session(self) -> FileSystemCatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return FileSystemCatalogStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# LocalFileSystemStoreSession
# -----------------------------------------------------------------------------


class FileSystemCatalogStoreSession(CatalogStoreSession):
    """A local file-system implementation of the MLTE catalog store."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage
        """The storage."""

        self.entry_mapper = FileSystemCatalogEntryMapper(storage=storage)
        """The mapper to entries CRUD."""

    def close(self) -> None:
        """Close the session."""
        # Closing a local FS session is a no-op.
        pass

    def read_entries(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        entry_ids = self.entry_mapper.list()
        return [
            CatalogEntry(**self.storage.read_resource(entry_id))
            for entry_id in entry_ids
        ][offset : offset + limit]

    def search_entries(
        self,
        query: Query = Query(),
    ) -> List[CatalogEntry]:
        entries = self.read_entries()
        return [entry for entry in entries if query.filter.match(entry)]


# -----------------------------------------------------------------------------
# FileSystemCatalogEntryMapper
# -----------------------------------------------------------------------------


class FileSystemCatalogEntryMapper(CatalogEntryMapper):
    """FS mapper for the catalog entry resource."""

    ENTRIES_FOLDER = "entries"
    """Subfolder for entries."""

    def __init__(self, storage: FileSystemStorage) -> None:
        self.storage = storage.clone()
        """A reference to underlying storage."""

        self.storage.set_base_path(
            Path(
                FileSystemCatalogStore.BASE_CATALOG_FOLDER, self.ENTRIES_FOLDER
            )
        )
        """Set the subfodler for this resrouce."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        self.storage.ensure_resource_does_not_exist(entry.header.identifier)
        return self._write_entry(entry)

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        self.storage.ensure_resource_exists(entry.header.identifier)
        return self._write_entry(entry)

    def read(self, entry_id: str) -> CatalogEntry:
        return self._read_entry(entry_id)

    def list(self) -> List[str]:
        return self.storage.list_resources()

    def delete(self, entry_id: str) -> CatalogEntry:
        self.storage.ensure_resource_exists(entry_id)
        entry = self._read_entry(entry_id)
        self.storage.delete_resource(entry_id)
        return entry

    def _read_entry(self, entry_id: str) -> CatalogEntry:
        """Reads a catalog entry."""
        self.storage.ensure_resource_exists(entry_id)
        return CatalogEntry(**self.storage.read_resource(entry_id))

    def _write_entry(self, entry: CatalogEntry) -> CatalogEntry:
        """Writes a entry to storage."""
        self.storage.write_resource(entry.header.identifier, entry.model_dump())
        return self._read_entry(entry.header.identifier)
