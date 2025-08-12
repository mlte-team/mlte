"""Unit tests for store query functionality."""

from mlte.catalog.model import CatalogEntry, CatalogEntryHeader
from mlte.store.query import (
    AllFilter,
    AndFilter,
    IdentifierFilter,
    NoneFilter,
    OrFilter,
    PropertyFilter,
    TagFilter,
)


class QACategoryPropertyFilter(PropertyFilter):
    name: str = "qa_category"


def create_test_entry(id: str = "def_id") -> CatalogEntry:
    entry = CatalogEntry(
        header=CatalogEntryHeader(identifier=id),
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


def test_qa_category_match() -> None:
    """The filter matches expected entries."""
    entry = create_test_entry()
    entry.tags = ["type1", "type2"]
    entry.qa_category = "cat1"

    filter1 = TagFilter(name="tags", value="type1")
    assert filter1.match(entry)

    filter1 = TagFilter(name="tags", value="type2")
    assert filter1.match(entry)

    filter1 = TagFilter(name="tags", value="type3")
    assert not filter1.match(entry)

    filter3 = QACategoryPropertyFilter(value="cat1")
    assert filter3.match(entry)

    filter3 = QACategoryPropertyFilter(value="cat3")
    assert not filter3.match(entry)


def test_and_match() -> None:
    """The and filter matches the expected entries."""
    a = create_test_entry("id0")
    b = create_test_entry("id0")
    c = create_test_entry("id3")

    filter = AndFilter(
        filters=[
            IdentifierFilter(id="id0"),
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
