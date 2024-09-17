"""
mlte/store/catalog/underlying/rdbs/reader.py

DB utils for getting catalog related data from the DB.
"""
from __future__ import annotations

import json
import typing
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

import mlte.store.error as errors
from mlte.catalog.model import (
    CatalogEntry,
    CatalogEntryHeader,
    CatalogEntryType,
)
from mlte.store.catalog.underlying.rdbs.metadata import (
    DBCatalogEntry,
    DBCatalogEntryHeader,
    DBCatalogEntryType,
)


class DBReader:
    """Class encapsulating functions to read catalog related data from the DB."""

    @staticmethod
    def get_entry(
        entry_id: str, session: Session
    ) -> Tuple[CatalogEntry, DBCatalogEntry]:
        """Reads the entry with the given id using the provided session, and returns a CatalogEntry and DBCatalogEntry object."""
        entry_obj = session.scalar(
            select(DBCatalogEntry)
            .where(DBCatalogEntry.entry_header_id == DBCatalogEntryHeader.id)
            .where(DBCatalogEntryHeader.identifier == entry_id)
        )

        if entry_obj is None:
            raise errors.ErrorNotFound(
                f"Entry with identifier {entry_id} was not found in the catalog store."
            )
        else:
            return (DBReader._build_entry(entry_obj), entry_obj)

    @staticmethod
    def _build_entry(
        entry_obj: DBCatalogEntry,
    ) -> CatalogEntry:
        """Builds a CatalogEntry object out of its DB model."""
        entry_header = CatalogEntryHeader(
            identifier=entry_obj.entry_header.identifier,
            creator=entry_obj.entry_header.creator,
            created=entry_obj.entry_header.created,
            updated=entry_obj.entry_header.updated,
            catalog_id=entry_obj.entry_header.catalog_identifier,
        )

        return CatalogEntry(
            tags=json.loads(entry_obj.tags),
            property_category=entry_obj.property_category,
            property=entry_obj.property,
            code=entry_obj.code,
            description=entry_obj.description,
            inputs=entry_obj.inputs,
            output=entry_obj.outputs,
            code_type=CatalogEntryType(entry_obj.catalog_entry_type.name),
            header=entry_header,
        )

    @staticmethod
    def _build_entry_obj(
        entry: CatalogEntry,
        session: Session,
        entry_obj: Optional[DBCatalogEntry] = None,
    ) -> DBCatalogEntry:
        """Creates a DB catalog entry object from a model."""
        if entry_obj is None:
            entry_obj = DBCatalogEntry()
            entry_header_obj = DBCatalogEntryHeader()
        else:
            entry_header_obj = entry_obj.entry_header

        entry_type_obj = (
            DBReader.get_entry_type(entry.code_type, session)
            if entry.code_type is not None
            else None
        )

        entry_header_obj.identifier = entry.header.identifier
        entry_header_obj.created = typing.cast(int, entry.header.created)
        entry_header_obj.updated = typing.cast(int, entry.header.updated)
        entry_header_obj.creator = entry.header.creator
        entry_header_obj.catalog_identifier = entry.header.catalog_id

        entry_obj.tags = json.dumps(entry.tags)
        entry_obj.property_category = entry.property_category
        entry_obj.property = entry.property
        entry_obj.code = entry.code
        entry_obj.description = entry.description
        entry_obj.inputs = entry.inputs
        entry_obj.outputs = entry.output
        entry_obj.catalog_entry_type = entry_type_obj
        entry_obj.entry_header = entry_header_obj

        return entry_obj

    @staticmethod
    def get_entries(
        session: Session,
    ) -> Tuple[List[CatalogEntry], List[DBCatalogEntry]]:
        """Reads all catalog entries in the DB, and returns a list of CatalogEntry and DBCatalogEntry objects."""
        entries_obj = list(
            session.execute(select(DBCatalogEntry)).scalars().all()
        )
        entries: List[CatalogEntry] = []
        for entry_obj in entries_obj:
            entry = DBReader._build_entry(entry_obj)
            entries.append(entry)

        return entries, entries_obj

    @staticmethod
    def get_entry_type(
        type: CatalogEntryType, session: Session
    ) -> DBCatalogEntryType:
        """Gets the catalog entry type DB object corresponding to the given internal type."""
        type_obj = session.scalar(
            select(DBCatalogEntryType).where(DBCatalogEntryType.name == type)
        )

        if type_obj is None:
            raise Exception(f"Unknown catalog etnry type requested: {type}")
        return type_obj
