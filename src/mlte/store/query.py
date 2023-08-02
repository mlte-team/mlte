"""
mlte/store/query.py

Query and filtering functionality for store operations.
"""

import typing

from enum import Enum
from mlte.artifact.model import ArtifactModel, ArtifactType

# -----------------------------------------------------------------------------
# ArtifactFilter
# -----------------------------------------------------------------------------


class FilterType(Enum):
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


class ArtifactFilter:
    """A general-purpose"""

    def __init__(self, *, type: FilterType) -> None:
        self.type = type
        """The filter type identifier."""

    def match(self, _: ArtifactModel) -> bool:
        """
        Determine if an artifact satisfies the filter.
        :param artifact: The artifact against which the match is tested
        :return: `True` if the filter is satisfied, `False` otherwise
        """
        raise NotImplementedError(
            "match() not implemented for abstract ArtifactFilter."
        )

    def to_query_string(self) -> str:
        """
        Convert a filter to an HTTP query string.
        :return: The query string
        """
        raise NotImplementedError(
            "to_query_string() not implemented for abstract ArtifactFilter."
        )


class ArtifactIdentifierFilter(ArtifactFilter):
    """A filter that matches an artifact identifier."""

    def __init__(self, *, artifact_id: str) -> None:
        super().__init__(type=FilterType.IDENTIFIER)

        self.artifact_id = artifact_id
        """The artifact identifier to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.identifier == self.artifact_id

    def to_query_string(self) -> str:
        return f"artifact_id={self.artifact_id}"

    def __str__(self) -> str:
        return f"identifier={self.artifact_id}"


class ArtifactTypeFilter(ArtifactFilter):
    """A filter that matches an artifact type."""

    def __init__(self, *, artifact_type: ArtifactType) -> None:
        super().__init__(type=FilterType.TYPE)

        self.artifact_type = artifact_type
        """The artifact type to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.type == self.artifact_type

    def to_query_string(self) -> str:
        return f"artifact_type={self.artifact_type}"

    def __str__(self) -> str:
        return f"type={self.artifact_type}"


class AndFilter(ArtifactFilter):
    """A generic filter that implements a logical AND of filters."""

    def __init__(self, *filters: ArtifactFilter) -> None:
        super().__init__(type=FilterType.AND)

        processed: list[ArtifactFilter] = []
        for filter in filters:
            if filter.type == FilterType.AND:
                and_filter = typing.cast(AndFilter, filter)
                processed.extend(and_filter.filters)  # type: ignore
            else:
                processed.append(filter)

        self.filters = processed
        """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return all(filter.match(artifact) for filter in self.filters)

    def to_query_string(self) -> str:
        return "&".join(filter.to_query_string() for filter in self.filters)

    def __str__(self) -> str:
        return " and ".join(f"{filter}" for filter in self.filters)


class OrFilter(ArtifactFilter):
    """A generic filter that implements a logical OR of filters."""

    def __init__(self, *filters: ArtifactFilter) -> None:
        super().__init__(type=FilterType.OR)

        processed: list[ArtifactFilter] = []
        for filter in filters:
            if filter.type == FilterType.OR:
                or_filter = typing.cast(OrFilter, filter)
                processed.extend(or_filter.filters)  # type: ignore
            else:
                processed.append(filter)

        self.filters = processed
        """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return any(filter.match(artifact) for filter in self.filters)

    def to_query_string(self) -> str:
        raise NotImplementedError(
            "to_query_string() not implemented for abstract OrFilter."
        )

    def __str__(self) -> str:
        return " or ".join(f"{filter}" for filter in self.filters)


class AllFilter(ArtifactFilter):
    """A filter that matches all artifacts."""

    def __init__(self) -> None:
        super().__init__(type=FilterType.ALL)

    def match(self, _: ArtifactModel) -> bool:
        return True

    def to_query_string(self) -> str:
        return ""

    def __str__(self) -> str:
        return "ALL"


class NoneFilter(ArtifactFilter):
    """A filter that matches no artifacts."""

    def __init__(self) -> None:
        super().__init__(type=FilterType.NONE)

    def match(self, _: ArtifactModel) -> bool:
        return False

    def to_query_string(self) -> str:
        raise NotImplementedError(
            "to_query_string() not implemented for abstract NoneFilter."
        )

    def __str__(self) -> str:
        return "NONE"
