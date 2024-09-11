"""
mlte/store/common/query.py

Query and filtering functionality for store operations.
"""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import Any, List, Literal, Union

from mlte.model import BaseModel

# Alias for all supported filters.
SupportedFilter = Union[
    "IdentifierFilter",
    "TypeFilter",
    "AllFilter",
    "NoneFilter",
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
        raise NotImplementedError(
            "Can't call get id without a specific implementation."
        )

    @abstractmethod
    def get_type(self) -> Any:
        raise NotImplementedError(
            "Can't call get type without a specific implementation."
        )


# -----------------------------------------------------------------------------
# Filters
# -----------------------------------------------------------------------------


class FilterType(str, Enum):
    """An enumeration over filter types."""

    IDENTIFIER = "identifier"
    TYPE = "type"
    ALL = "all"
    NONE = "none"
    AND = "and"
    OR = "or"


class IdentifierFilter(Filter):
    """A filter that matches an catalog entry identifier."""

    type: Literal[FilterType.IDENTIFIER] = FilterType.IDENTIFIER
    """An identifier for the filter type."""

    id: str
    """The identifier to match."""

    def match(self, item: Filtrable) -> bool:
        return bool(item.get_identifier() == self.id)


class TypeFilter(Filter):
    """A filter that matches an catalog entry type."""

    type: Literal[FilterType.TYPE] = FilterType.TYPE
    """An identifier for the filter type."""

    item_type: Any
    """The type to match."""

    def match(self, item: Filtrable) -> bool:
        return bool(item.get_type() == self.item_type)


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
