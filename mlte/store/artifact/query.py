"""
mlte/store/artifact/query.py

Query and filtering functionality for store operations.
"""

from __future__ import annotations

from typing import List, Union

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.store.common.query import (
    AllFilter,
    AndFilter,
    IdentifierFilter,
    NoneFilter,
    OrFilter,
    TypeFilter,
)

# A type alias
ArtifactFilter = Union[
    AllFilter,
    NoneFilter,
    "ArtifactIdentifierFilter",
    "ArtifactTypeFilter",
    "ArtifactAndFilter",
    "ArtifactOrFilter",
]


class ArtifactIdentifierFilter(IdentifierFilter):
    """A filter that matches an artifact identifier."""

    artifact_id: str
    """The artifact identifier to match."""

    def match(self, artifact: ArtifactModel) -> bool:  # type: ignore
        return artifact.header.identifier == self.artifact_id


class ArtifactTypeFilter(TypeFilter):
    """A filter that matches an artifact type."""

    artifact_type: ArtifactType
    """The artifact type to match."""

    def match(self, artifact: ArtifactModel) -> bool:  # type: ignore
        return artifact.header.type == self.artifact_type


class ArtifactAndFilter(AndFilter):
    """AndFilter subclass for artifact filters."""

    filters: List[ArtifactFilter]  # type: ignore


class ArtifactOrFilter(OrFilter):
    """OrFilter subclass for artifact filters."""

    filters: List[ArtifactFilter]  # type: ignore


# Necessary for pydantic to resolve forward references
ArtifactAndFilter.model_rebuild()
ArtifactOrFilter.model_rebuild()
