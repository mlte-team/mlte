"""
mlte/store/query.py

Query and filtering functionality for store operations.
"""

from typing import Union, Literal

from mlte.model import BaseModel
from enum import Enum
from mlte.artifact.model import ArtifactModel, ArtifactType

# A type alias
Filter = Union[
    "ArtifactIdentifierFilter",
    "ArtifactTypeFilter",
    "AndFilter",
    "OrFilter",
    "AllFilter",
    "NoneFilter",
]

# -----------------------------------------------------------------------------
# ArtifactFilter
# -----------------------------------------------------------------------------


class FilterType(str, Enum):
    """An enumeration over filter types."""

    IDENTIFIER = "identifier"
    """A filter over artifact identifiers."""

    TYPE = "type"
    """A filter over artifact types."""

    ALL = "all"
    """The 'all' filter."""

    NONE = "none"
    """The 'none' filter."""

    AND = "and"
    """The 'and' filter."""

    OR = "or"
    """The 'or' filter."""


class ArtifactIdentifierFilter(BaseModel):
    """A filter that matches an artifact identifier."""

    type: Literal[FilterType.IDENTIFIER]
    """An identifier for the filter type."""

    artifact_id: str
    """The artifact identifier to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.identifier == self.artifact_id


class ArtifactTypeFilter(BaseModel):
    """A filter that matches an artifact type."""

    type: Literal[FilterType.TYPE]
    """An identifier for the filter type."""

    artifact_type: ArtifactType
    """The artifact type to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.type == self.artifact_type


class AllFilter(BaseModel):
    """A filter that matches all artifacts."""

    type: Literal[FilterType.ALL]
    """An identifier for the filter type."""

    def match(self, _: ArtifactModel) -> bool:
        return True


class NoneFilter(BaseModel):
    """A filter that matches no artifacts."""

    type: Literal[FilterType.NONE]
    """An identifier for the filter type."""

    def match(self, _: ArtifactModel) -> bool:
        return False


class AndFilter(BaseModel):
    """A generic filter that implements a logical AND of filters."""

    type: Literal[FilterType.AND]
    """An identifier for the filter type."""

    filters: list[Filter]
    """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return all(filter.match(artifact) for filter in self.filters)


class OrFilter(BaseModel):
    """A generic filter that implements a logical OR of filters."""

    type: Literal[FilterType.OR]
    """An identifier for the filter type."""

    filters: list[Filter]
    """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return any(filter.match(artifact) for filter in self.filters)


class Query(BaseModel):
    """A Query object represents a query over MLTE artifacts."""

    filter: Filter
    """The filter that is applied to implement the query."""

    def __init__(
        self, *, filter: Filter = AllFilter(type=FilterType.ALL)
    ) -> None:
        super().__init__(filter=filter)


# Necessary for pydantic to resolve forward references
AndFilter.update_forward_refs()
OrFilter.update_forward_refs()
