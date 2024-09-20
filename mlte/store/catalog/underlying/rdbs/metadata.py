"""
mlte/store/catalog/underlying/rdbs/metadata.py

Definition of the metadata (DB schema) for the catalog store.
"""
from __future__ import annotations

from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from mlte.catalog.model import CatalogEntryType


class DBBase(DeclarativeBase):
    """Base class for DB table classes."""

    pass


class DBCatalogEntryType(DBBase):
    __tablename__ = "catalog_entry_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"CatalgoEntryType(id={self.id!r}, name={self.name!r})"


class DBCatalogEntryHeader(DBBase):
    __tablename__ = "catalog_entry_header"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier: Mapped[str]
    created: Mapped[int] = mapped_column(BigInteger)
    updated: Mapped[int] = mapped_column(BigInteger)
    creator: Mapped[Optional[str]]
    catalog_identifier: Mapped[Optional[str]]

    body: Mapped[Optional[DBCatalogEntry]] = relationship(
        back_populates="entry_header", cascade="all"
    )

    def __repr__(self) -> str:
        return f"CatalogEntryHeader(id={self.id!r}, identifier={self.identifier!r}, created={self.created!r}, updated={self.updated!r}, creator={self.creator!r})"


class DBCatalogEntry(DBBase):
    __tablename__ = "catalog_entry"

    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[str]
    property_category: Mapped[Optional[str]]
    property: Mapped[Optional[str]]
    code: Mapped[str]
    description: Mapped[Optional[str]]
    inputs: Mapped[Optional[str]]
    outputs: Mapped[Optional[str]]

    entry_header_id: Mapped[int] = mapped_column(
        ForeignKey("catalog_entry_header.id")
    )
    entry_header: Mapped[DBCatalogEntryHeader] = relationship(
        back_populates="body", cascade="all"
    )

    catalog_entry_type_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("catalog_entry_type.id")
    )
    catalog_entry_type: Mapped[DBCatalogEntryType] = relationship()

    def __repr__(self) -> str:
        return f"CatalogEntry(id={self.id!r}, description={self.description!r}, code={self.code!r}, property_category={self.property_category}, property={self.property!r})"


# -------------------------------------------------------------------------
# Pre-filled table functions.
# -------------------------------------------------------------------------


def init_catalog_entry_types(session: Session):
    """Initializes the table with the configured catalog entry types."""
    if session.scalars(select(DBCatalogEntryType)).first() is None:
        types = [e.value for e in CatalogEntryType]
        for type in types:
            type_obj = DBCatalogEntryType(name=type)
            session.add(type_obj)
        session.commit()
