"""
mlte/store/artifact/query.py

Query and filtering functionality for store operations.
"""

from __future__ import annotations

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.store.common.query import IdentifierFilter, TypeFilter


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
