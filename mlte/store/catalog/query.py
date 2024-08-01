"""
mlte/store/catalog/query.py

Query and filtering functionality for catalog store operations.
"""

from __future__ import annotations

from typing import List, Union

from mlte.catalog.model import CatalogEntry, CatalogEntryType
from mlte.store.common.query import (
    AllFilter,
    AndFilter,
    IdentifierFilter,
    NoneFilter,
    OrFilter,
    TypeFilter,
)

# A type alias
CatalogEntryFilter = Union[
    AllFilter,
    NoneFilter,
    "CatalogEntryIdentifierFilter",
    "CatalogEntryTypeFilter",
    "CatalogEntryAndFilter",
    "CatalogEntryOrFilter",
]


class CatalogEntryIdentifierFilter(IdentifierFilter):
    """A filter that matches an catalog entry identifier."""

    catalog_entry_id: str
    """The catalog entry identifier to match."""

    def match(self, catalog_entry: CatalogEntry) -> bool:  # type: ignore
        return catalog_entry.header.identifier == self.catalog_entry_id


class CatalogEntryTypeFilter(TypeFilter):
    """A filter that matches an catalog entry type."""

    catalog_entry_type: CatalogEntryType
    """The catalog entry type to match."""

    def match(self, catalog_entry: CatalogEntry) -> bool:  # type: ignore
        return catalog_entry.code_type == self.catalog_entry_type


class CatalogEntryAndFilter(AndFilter):
    """AndFilter subclass for catalog entry filters."""

    filters: List[CatalogEntryFilter]  # type: ignore


class CatalogEntryOrFilter(OrFilter):
    """OrFilter subclass for catalog entry filters."""

    filters: List[CatalogEntryFilter]  # type: ignore


# Necessary for pydantic to resolve forward references
CatalogEntryAndFilter.model_rebuild()
CatalogEntryOrFilter.model_rebuild()
