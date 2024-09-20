"""
test/store/catalog/test_query.py

Unit tests for store query functionality.
"""

from mlte.catalog.model import (
    CatalogEntry,
    CatalogEntryHeader,
    CatalogEntryType,
)
from mlte.store.query import (
    AllFilter,
    AndFilter,
    IdentifierFilter,
    NoneFilter,
    OrFilter,
    PropertyFilter,
    TagFilter,
    TypeFilter,
)


class PropertyCategoryPropertyFilter(PropertyFilter):
    name: str = "property_category"


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
    entry = create_test_entry()
    assert AllFilter().match(entry)


def test_none_match() -> None:
    """The none filter matches no entries."""
    entry = create_test_entry()
    assert not NoneFilter().match(entry)


def test_identifier_match() -> None:
    """The identifier filter matches the expected entries."""
    a = create_test_entry("id0")
    b = create_test_entry("id1")

    filter = IdentifierFilter(id="id0")
    assert filter.match(a)
    assert not filter.match(b)


def test_type_match() -> None:
    """The type filter matches expected entries."""
    entry = create_test_entry(type=CatalogEntryType.MEASUREMENT)

    filter = TypeFilter(item_type=CatalogEntryType.MEASUREMENT)
    assert filter.match(entry)

    filter = TypeFilter(item_type=CatalogEntryType.VALIDATION)
    assert not filter.match(entry)


def test_property_match() -> None:
    """The filter matches expected entries."""
    entry = create_test_entry(type=CatalogEntryType.MEASUREMENT)
    entry.tags = ["type1", "type2"]
    entry.property_category = "cat1"

    filter1 = TagFilter(name="tags", value="type1")
    assert filter1.match(entry)

    filter1 = TagFilter(name="tags", value="type2")
    assert filter1.match(entry)

    filter1 = TagFilter(name="tags", value="type3")
    assert not filter1.match(entry)

    filter3 = PropertyCategoryPropertyFilter(value="cat1")
    assert filter3.match(entry)

    filter3 = PropertyCategoryPropertyFilter(value="cat3")
    assert not filter3.match(entry)


def test_and_match() -> None:
    """The and filter matches the expected entries."""
    a = create_test_entry("id0", type=CatalogEntryType.MEASUREMENT)
    b = create_test_entry("id0", type=CatalogEntryType.VALIDATION)
    c = create_test_entry("id3", type=CatalogEntryType.MEASUREMENT)

    filter = AndFilter(
        filters=[
            IdentifierFilter(id="id0"),
            TypeFilter(item_type=CatalogEntryType.MEASUREMENT),
        ],
    )

    assert filter.match(a)
    assert not filter.match(b)
    assert not filter.match(c)


def test_or_match() -> None:
    """The or filter matches the expected entries."""
    a = create_test_entry("id0")
    b = create_test_entry("id1")
    c = create_test_entry("id3")

    filter = OrFilter(
        filters=[
            IdentifierFilter(id="id0"),
            IdentifierFilter(id="id1"),
        ],
    )

    assert filter.match(a)
    assert filter.match(b)
    assert not filter.match(c)
