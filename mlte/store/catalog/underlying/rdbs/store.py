"""
mlte/store/catalog/underlying/rdbs/store.py

Implementation of relational database system catalog store.
"""
from __future__ import annotations

from typing import List

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy_utils
from sqlalchemy import Engine
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
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

# -----------------------------------------------------------------------------
# RelationalDBCatalogStore
# -----------------------------------------------------------------------------


class RelationalDBCatalogStore(CatalogStore):
    """A DB implementation of the MLTE user store."""

    def __init__(self, uri: StoreURI, **kwargs) -> None:
        self.engine = sqlalchemy.create_engine(uri.uri, **kwargs)
        """The underlying storage for the store."""

        # Create the DB if it doesn't exist already.
        if not sqlalchemy_utils.database_exists(self.engine.url):
            sqlalchemy_utils.create_database(self.engine.url)

        # Creates the DB items if they don't exist already.
        self._create_tables()
        self._init_tables()

        # Intialize base defaults.
        super().__init__(uri=uri)

    def session(self) -> RelationalDBCatalogStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return RelationalDBCatalogStoreSession(engine=self.engine)

    def _create_tables(self):
        """Creates all items, if they don't exist already."""
        DBBase.metadata.create_all(self.engine)

    def _init_tables(self):
        """Pre-populate tables."""
        with Session(self.engine) as session:
            init_catalog_entry_types(session)


# -----------------------------------------------------------------------------
# RelationalDBCatalogStoreSession
# -----------------------------------------------------------------------------


class RelationalDBCatalogStoreSession(CatalogStoreSession):
    """A relational DB implementation of the MLTE user store session."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

        self.entry_mapper = RDBEntryMapper(engine)
        """The mapper to user CRUD."""

    def close(self) -> None:
        """Close the session."""
        self.engine.dispose()


# -----------------------------------------------------------------------------
# RDBEntryMapper
# -----------------------------------------------------------------------------


class RDBEntryMapper(CatalogEntryMapper):
    """RDB mapper for a catalog entry resource."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        """A reference to underlying storage."""

    def create(self, entry: CatalogEntry) -> CatalogEntry:
        with Session(self.engine) as session:
            try:
                _, _ = DBReader.get_entry(entry.header.identifier, session)
                raise errors.ErrorAlreadyExists(f"{entry} already exists.")
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
        with Session(self.engine) as session:
            _, entry_obj = DBReader.get_entry(entry.header.identifier, session)

            # Update existing user.
            entry_obj = DBReader._build_entry_obj(entry, session, entry_obj)
            session.commit()

            stored_entry, _ = DBReader.get_entry(
                entry.header.identifier, session
            )
            return stored_entry

    def read(self, entry_id: str) -> CatalogEntry:
        with Session(self.engine) as session:
            catalog_entry, _ = DBReader.get_entry(entry_id, session)
            return catalog_entry

    def list(self) -> List[str]:
        with Session(self.engine) as session:
            entries, _ = DBReader.get_entries(session)
            return [entry.header.identifier for entry in entries]

    def delete(self, entry_id: str) -> CatalogEntry:
        with Session(self.engine) as session:
            catalog_entry, entry_obj = DBReader.get_entry(entry_id, session)
            session.delete(entry_obj)
            session.commit()
            return catalog_entry
