"""
test/store/catalog/test_query.py

Unit tests for store query functionality.
"""

from mlte.catalog.model import (
    CatalogEntry,
    CatalogEntryHeader,
    CatalogEntryType,
)
from mlte.store.catalog.query import (
    CatalogEntryAndFilter,
    CatalogEntryIdentifierFilter,
    CatalogEntryOrFilter,
    CatalogEntryTypeFilter,
)
from mlte.store.common.query import AllFilter, NoneFilter


def create_test_entry(
    id: str = "def_id", type: CatalogEntryType = CatalogEntryType.MEASUREMENT
) -> CatalogEntry:
    entry = CatalogEntry(
        header=CatalogEntryHeader(identifier=id),
        code_type=type,
        code="hello world",
    )
    return entry


def test_all_match() -> None:
    """The all filter matches all entries."""
    e = create_test_entry()
    assert AllFilter().match(e)


def test_none_match() -> None:
    """The none filter matches no entries."""
    e = create_test_entry()
    assert not NoneFilter().match(e)


def test_identifier() -> None:
    """The identifier filter can be serialized and deserialized."""
    f = CatalogEntryIdentifierFilter(catalog_entry_id="id0")
    assert CatalogEntryIdentifierFilter(**f.model_dump()) == f


def test_identifier_match() -> None:
    """The identifier filter matches the expected entries."""
    a = create_test_entry("id0")
    b = create_test_entry("id1")

    filter = CatalogEntryIdentifierFilter(catalog_entry_id="id0")
    assert filter.match(a)
    assert not filter.match(b)


def test_type() -> None:
    """The type filter can be serialized and deserialized."""
    f = CatalogEntryTypeFilter(catalog_entry_type=CatalogEntryType.MEASUREMENT)
    assert CatalogEntryTypeFilter(**f.model_dump()) == f


def test_type_match() -> None:
    """The type filter matches expected entries."""
    a = create_test_entry(type=CatalogEntryType.MEASUREMENT)

    filter = CatalogEntryTypeFilter(
        catalog_entry_type=CatalogEntryType.MEASUREMENT
    )
    assert filter.match(a)

    filter = CatalogEntryTypeFilter(
        catalog_entry_type=CatalogEntryType.VALIDATION
    )
    assert not filter.match(a)


def test_and() -> None:
    """The AND filter can be serialized and deserialized."""
    f = CatalogEntryAndFilter(
        filters=[
            AllFilter(),
            NoneFilter(),
            CatalogEntryIdentifierFilter(catalog_entry_id="id0"),
            CatalogEntryTypeFilter(
                catalog_entry_type=CatalogEntryType.MEASUREMENT
            ),
        ],
    )
    assert CatalogEntryAndFilter(**f.model_dump()) == f


def test_and_match() -> None:
    """The and filter matches the expected entries."""
    a = create_test_entry("id0", type=CatalogEntryType.MEASUREMENT)
    b = create_test_entry("id0", type=CatalogEntryType.VALIDATION)
    c = create_test_entry("id3", type=CatalogEntryType.MEASUREMENT)

    filter = CatalogEntryAndFilter(
        filters=[
            CatalogEntryIdentifierFilter(catalog_entry_id="id0"),
            CatalogEntryTypeFilter(
                catalog_entry_type=CatalogEntryType.MEASUREMENT
            ),
        ],
    )

    assert filter.match(a)
    assert not filter.match(b)
    assert not filter.match(c)


def test_or() -> None:
    """The OR filter can be serialized and deserialized."""
    f = CatalogEntryOrFilter(
        filters=[
            AllFilter(),
            NoneFilter(),
            CatalogEntryIdentifierFilter(catalog_entry_id="id0"),
            CatalogEntryTypeFilter(
                catalog_entry_type=CatalogEntryType.MEASUREMENT
            ),
        ],
    )
    assert CatalogEntryOrFilter(**f.model_dump()) == f


def test_or_match() -> None:
    """The or filter matches the expected entries."""
    a = create_test_entry("id0")
    b = create_test_entry("id1")
    c = create_test_entry("id3")

    filter = CatalogEntryOrFilter(
        filters=[
            CatalogEntryIdentifierFilter(catalog_entry_id="id0"),
            CatalogEntryIdentifierFilter(catalog_entry_id="id1"),
        ],
    )

    assert filter.match(a)
    assert filter.match(b)
    assert not filter.match(c)
