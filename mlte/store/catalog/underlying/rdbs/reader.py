"""DB utils for getting catalog related data from the DB."""

from __future__ import annotations

import typing
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte._private.fixed_json import json
from mlte.catalog.model import CatalogEntry, CatalogEntryHeader
from mlte.store.catalog.underlying.rdbs.metadata import (
    DBCatalogEntry,
    DBCatalogEntryHeader,
)


class DBReader:
    """Class encapsulating functions to read catalog related data from the DB."""

    @staticmethod
    def get_entry(
        entry_id: str, session: Session
    ) -> Tuple[CatalogEntry, DBCatalogEntry]:
        """Reads the entry with the given id using the provided session, and returns a CatalogEntry and DBCatalogEntry object."""
        entry_orm = session.scalar(
            select(DBCatalogEntry)
            .where(DBCatalogEntry.entry_header_id == DBCatalogEntryHeader.id)
            .where(DBCatalogEntryHeader.identifier == entry_id)
        )

        if entry_orm is None:
            raise errors.ErrorNotFound(
                f"Entry with identifier {entry_id} was not found in the catalog store."
            )
        else:
            return (DBReader._build_entry(entry_orm), entry_orm)

    @staticmethod
    def _build_entry(
        entry_orm: DBCatalogEntry,
    ) -> CatalogEntry:
        """Builds a CatalogEntry object out of its DB model."""
        entry_header = CatalogEntryHeader(
            identifier=entry_orm.entry_header.identifier,
            creator=entry_orm.entry_header.creator,
            created=entry_orm.entry_header.created,
            updated=entry_orm.entry_header.updated,
            catalog_id=entry_orm.entry_header.catalog_identifier,
        )

        return CatalogEntry(
            tags=json.loads(entry_orm.tags),
            quality_attribute=entry_orm.quality_attribute,
            code=entry_orm.code,
            description=entry_orm.description,
            inputs=entry_orm.inputs,
            output=entry_orm.outputs,
            header=entry_header,
        )

    @staticmethod
    def _build_entry_orm(
        entry: CatalogEntry,
        session: Session,
        entry_orm: Optional[DBCatalogEntry] = None,
    ) -> DBCatalogEntry:
        """Creates or updates a DB catalog entry object from a model."""
        if entry_orm is None:
            entry_orm = DBCatalogEntry()
            entry_header_orm = DBCatalogEntryHeader()
        else:
            entry_header_orm = entry_orm.entry_header

        entry_header_orm.identifier = entry.header.identifier
        entry_header_orm.created = typing.cast(int, entry.header.created)
        entry_header_orm.updated = typing.cast(int, entry.header.updated)
        entry_header_orm.creator = entry.header.creator
        entry_header_orm.catalog_identifier = entry.header.catalog_id

        entry_orm.tags = json.dumps(entry.tags)
        entry_orm.quality_attribute = entry.quality_attribute
        entry_orm.code = entry.code
        entry_orm.description = entry.description
        entry_orm.inputs = entry.inputs
        entry_orm.outputs = entry.output
        entry_orm.entry_header = entry_header_orm

        return entry_orm

    @staticmethod
    def get_entries(
        session: Session,
    ) -> Tuple[List[CatalogEntry], List[DBCatalogEntry]]:
        """Reads all catalog entries in the DB, and returns a list of CatalogEntry and DBCatalogEntry objects."""
        entries_orm = list(
            session.execute(select(DBCatalogEntry)).scalars().all()
        )
        entries: List[CatalogEntry] = []
        for entry_orm in entries_orm:
            entry = DBReader._build_entry(entry_orm)
            entries.append(entry)

        return entries, entries_orm
