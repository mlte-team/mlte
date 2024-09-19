"""
mlte/store/catalog/underlying/rdbs/store.py

Implementation of relational database system catalog store.
"""
from __future__ import annotations

import typing
from typing import List

from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeBase, Session

import mlte.store.error as errors
from mlte.catalog.model import CatalogEntry
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.catalog.underlying.rdbs.metadata import (
    DBBase,
    init_catalog_entry_types,
)
from mlte.store.catalog.underlying.rdbs.reader import DBReader
from mlte.store.common.rdbs_storage import RDBStorage

# -----------------------------------------------------------------------------
# RelationalDBCatalogStore
# -----------------------------------------------------------------------------


class RelationalDBCatalogStore(CatalogStore):
    """A DB implementation of the MLTE user store."""

    def __init__(self, uri, **kwargs):
        CatalogStore.__init__(self, uri=uri)

        self.storage = RDBStorage(
            uri,
            base_class=typing.cast(DeclarativeBase, DBBase),
            init_tables_func=init_catalog_tables,
            **kwargs,
        )
        """The relational DB storage."""

    def session(self) -> RelationalDBCatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBCatalogStoreSession(
            storage=self.storage, read_only=self.read_only
        )


def init_catalog_tables(engine: Engine):
    """Pre-populate tables."""
    with Session(engine) as session:
        init_catalog_entry_types(session)


# -----------------------------------------------------------------------------
# RelationalDBCatalogStoreSession
# -----------------------------------------------------------------------------


class RelationalDBCatalogStoreSession(CatalogStoreSession):
    """A relational DB implementation of the MLTE user store session."""

    def __init__(self, storage: RDBStorage, read_only: bool = False) -> None:
        self.storage = storage
        """RDB storage."""

        self.read_only = read_only
        """Whether this is read only or not."""

        self.entry_mapper = RDBEntryMapper(storage)
        """The mapper to user CRUD."""

    def close(self) -> None:
        """Close the session."""
        self.storage.close()


# -----------------------------------------------------------------------------
# RDBEntryMapper
# -----------------------------------------------------------------------------


class RDBEntryMapper(CatalogEntryMapper):
    """RDB mapper for a catalog entry resource."""

    def __init__(self, storage: RDBStorage) -> None:
        self.storage = storage
        """A reference to underlying storage."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        with Session(self.storage.engine) as session:
            try:
                _, _ = DBReader.get_entry(entry.header.identifier, session)
                raise errors.ErrorAlreadyExists(
                    f"Entry with id {entry.header.identifier} already exists."
                )
            except errors.ErrorNotFound:
                # If it was not found, it means we can create it.
                entry_obj = DBReader._build_entry_obj(entry, session)
                session.add(entry_obj)
                session.commit()

                stored_entry, _ = DBReader.get_entry(
                    entry.header.identifier, session
                )
                return stored_entry

    def edit(self, entry: CatalogEntry) -> CatalogEntry:
        with Session(self.storage.engine) as session:
            _, entry_obj = DBReader.get_entry(entry.header.identifier, session)

            # Update existing user.
            entry_obj = DBReader._build_entry_obj(entry, session, entry_obj)
            session.commit()

            stored_entry, _ = DBReader.get_entry(
                entry.header.identifier, session
            )
            return stored_entry

    def read(self, entry_id: str) -> CatalogEntry:
        with Session(self.storage.engine) as session:
            catalog_entry, _ = DBReader.get_entry(entry_id, session)
            return catalog_entry

    def list(self) -> List[str]:
        with Session(self.storage.engine) as session:
            entries, _ = DBReader.get_entries(session)
            return [entry.header.identifier for entry in entries]

    def delete(self, entry_id: str) -> CatalogEntry:
        with Session(self.storage.engine) as session:
            catalog_entry, entry_obj = DBReader.get_entry(entry_id, session)
            session.delete(entry_obj)
            session.commit()
            return catalog_entry
