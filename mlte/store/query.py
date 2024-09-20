"""
mlte/store/common/query.py

Query and filtering functionality for store operations.
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, List, Literal, Union

from strenum import LowercaseStrEnum

import mlte.store.error as errors
from mlte.model import BaseModel

# Alias for all supported filters.
SupportedFilter = Union[
    "AllFilter",
    "NoneFilter",
    "IdentifierFilter",
    "TypeFilter",
    "TagFilter",
    "PropertyFilter",
    "AndFilter",
    "OrFilter",
]


class Filter(BaseModel):
    """Definition of a filter interface."""

    @abstractmethod
    def match(self, item: Filtrable) -> bool:
        raise NotImplementedError(
            "Can't call match without a specific implementation."
        )


class CompositeFilter(Filter):
    """Definition of a composite filter interface."""

    filters: List[SupportedFilter]


class Filtrable(BaseModel):
    """Definition of a filtrable interface."""

    @abstractmethod
    def get_identifier(self) -> str:
        """Returns the identifier for filtering."""
        raise NotImplementedError(
            "Can't call get id without a specific implementation."
        )

    @abstractmethod
    def get_type(self) -> Any:
        """Returns the class-specific type for filtering."""
        raise NotImplementedError(
            "Can't call get type without a specific implementation."
        )

    def get_property(self, property_name: str) -> Any:
        """Returns the given property."""
        try:
            value = getattr(self, property_name)
            return value
        except Exception:
            raise errors.ErrorNotFound(
                f"Property '{property_name}' is not part of the model."
            )

    def get_tags(self, property_name: str) -> List[Any]:
        """Returns the given tags."""
        value = self.get_property(property_name)
        if type(value) is not list:
            raise RuntimeError(
                f"Property {property_name} does not contain a list of tags."
            )
        else:
            return value


# -----------------------------------------------------------------------------
# Filters
# -----------------------------------------------------------------------------


class FilterType(LowercaseStrEnum):
    """An enumeration over filter types."""

    IDENTIFIER = "identifier"
    TYPE = "type"
    TAG = "tag"
    PROPERTY = "property"
    ALL = "all"
    NONE = "none"
    AND = "and"
    OR = "or"


class AllFilter(Filter):
    """A filter that matches all entries."""

    type: Literal[FilterType.ALL] = FilterType.ALL
    """An identifier for the filter type."""

    def match(self, _: Filtrable) -> bool:
        return True


class NoneFilter(Filter):
    """A filter that matches no entries."""

    type: Literal[FilterType.NONE] = FilterType.NONE
    """An identifier for the filter type."""

    def match(self, _: Filtrable) -> bool:
        return False


class IdentifierFilter(Filter):
    """A filter that matches an item's identifier."""

    type: Literal[FilterType.IDENTIFIER] = FilterType.IDENTIFIER
    """An identifier for the filter type."""

    id: str
    """The identifier to match."""

    def match(self, item: Filtrable) -> bool:
        return bool(item.get_identifier() == self.id)


class TypeFilter(Filter):
    """A filter that matches an item's type."""

    type: Literal[FilterType.TYPE] = FilterType.TYPE
    """An identifier for the filter type."""

    item_type: Any
    """The type to match."""

    def match(self, item: Filtrable) -> bool:
        return bool(item.get_type() == self.item_type)


class TagFilter(Filter):
    """A filter that matches a given tag, from a field with a list of tags."""

    type: Literal[FilterType.TAG] = FilterType.TAG
    """An identifier for the filter type."""

    name: str
    """The name of the property with the tags."""

    value: Any
    """The property to match."""

    def match(self, item: Filtrable) -> bool:
        return self.value in item.get_tags(self.name)


class PropertyFilter(Filter):
    """A filter that matches a given property."""

    type: Literal[FilterType.PROPERTY] = FilterType.PROPERTY
    """An identifier for the filter type."""

    name: str
    """The name of the property."""

    value: Any
    """The property to match."""

    def match(self, item: Filtrable) -> bool:
        return bool(self.value in item.get_property(self.name))


class AndFilter(CompositeFilter):
    """A generic filter that implements a logical AND of filters."""

    type: Literal[FilterType.AND] = FilterType.AND
    """An identifier for the filter type."""

    def match(self, item: Filtrable) -> bool:
        return all(filter.match(item) for filter in self.filters)


class OrFilter(CompositeFilter):
    """A generic filter that implements a logical OR of filters."""

    type: Literal[FilterType.OR] = FilterType.OR
    """An identifier for the filter type."""

    def match(self, item: Filtrable) -> bool:
        return any(filter.match(item) for filter in self.filters)


class Query(BaseModel):
    """A Query object represents a query over entries."""

    filter: SupportedFilter = AllFilter()
    """The filter that is applied to implement the query."""


# Necessary for pydantic to resolve forward references
AndFilter.model_rebuild()
OrFilter.model_rebuild()
