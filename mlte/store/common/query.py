"""
mlte/store/common/query.py

Query and filtering functionality for store operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Literal, Union

from mlte.model import BaseModel

# A type alias
Filter = Union[
    "IdentifierFilter",
    "TypeFilter",
    "AndFilter",
    "OrFilter",
    "AllFilter",
    "NoneFilter",
]

# -----------------------------------------------------------------------------
# Filters
# -----------------------------------------------------------------------------


class FilterType(str, Enum):
    """An enumeration over filter types."""

    IDENTIFIER = "identifier"
    """A filter over item identifiers."""

    TYPE = "type"
    """A filter over item types."""

    ALL = "all"
    """The 'all' filter."""

    NONE = "none"
    """The 'none' filter."""

    AND = "and"
    """The 'and' filter."""

    OR = "or"
    """The 'or' filter."""


class IdentifierFilter(BaseModel, ABC):
    """A filter that matches an catalog entry identifier."""

    type: Literal[FilterType.IDENTIFIER] = FilterType.IDENTIFIER
    """An identifier for the filter type."""

    @abstractmethod
    def match(self, item: BaseModel) -> bool:
        raise NotImplementedError(
            "Can't match on abstract base IdentifierFilter"
        )


class TypeFilter(BaseModel, ABC):
    """A filter that matches an catalog entry type."""

    type: Literal[FilterType.TYPE] = FilterType.TYPE
    """An identifier for the filter type."""

    @abstractmethod
    def match(self, item: BaseModel) -> bool:
        raise NotImplementedError("Can't match on abstract base TypeFilter")


class AllFilter(BaseModel):
    """A filter that matches all entries."""

    type: Literal[FilterType.ALL] = FilterType.ALL
    """An identifier for the filter type."""

    def match(self, _: BaseModel) -> bool:
        return True


class NoneFilter(BaseModel):
    """A filter that matches no entries."""

    type: Literal[FilterType.NONE] = FilterType.NONE
    """An identifier for the filter type."""

    def match(self, _: BaseModel) -> bool:
        return False


class AndFilter(BaseModel):
    """A generic filter that implements a logical AND of filters."""

    type: Literal[FilterType.AND] = FilterType.AND
    """An identifier for the filter type."""

    filters: List[Filter]
    """The filters of which the composition is composed."""

    def match(self, item: BaseModel) -> bool:
        return all(filter.match(item) for filter in self.filters)


class OrFilter(BaseModel):
    """A generic filter that implements a logical OR of filters."""

    type: Literal[FilterType.OR] = FilterType.OR
    """An identifier for the filter type."""

    filters: List[Filter]
    """The filters of which the composition is composed."""

    def match(self, item: BaseModel) -> bool:
        return any(filter.match(item) for filter in self.filters)


class Query(BaseModel):
    """A Query object represents a query over entries."""

    filter: Filter = AllFilter(type=FilterType.ALL)
    """The filter that is applied to implement the query."""


# Necessary for pydantic to resolve forward references
AndFilter.model_rebuild()
OrFilter.model_rebuild()
