"""
mlte/store/catalog/query.py

Query and filtering functionality for catalog store operations.
"""

from __future__ import annotations

from mlte.catalog.model import CatalogEntry, CatalogEntryType
from mlte.store.common.query import IdentifierFilter, TypeFilter


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
