"""
mlte/store/query.py

Query and filtering functionality for store operations.
"""

from typing import Optional
from mlte.artifact.model import ArtifactModel, ArtifactType

# -----------------------------------------------------------------------------
# ArtifactFilter
# -----------------------------------------------------------------------------


class ArtifactFilter:
    """A general-purpose"""

    def __init__(
        self,
        *,
        artifact_id: Optional[str] = None,
        artifact_type: Optional[ArtifactType] = None,
    ) -> None:
        self.artifact_id = artifact_id
        """The artifact identifier filter."""

        self.artifact_type = artifact_type
        """The artifact type filter."""

    def match(self, _: ArtifactModel) -> bool:
        """
        Determine if an artifact satisfies the filter.
        :param artifact: The artifact against which the match is tested
        :return: `True` if the filter is satisfied, `False` otherwise
        """
        raise NotImplementedError(
            "match() not implemented for abstract ArtifactFilter."
        )


class ArtifactIdentifierFilter(ArtifactFilter):
    """A filter that matches an artifact identifier."""

    def __init__(self, *, artifact_id: str) -> None:
        self.artifact_id = artifact_id
        """The artifact identifier to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.identifier == self.artifact_id


class ArtifactTypeFilter(ArtifactFilter):
    """A filter that matches an artifact type."""

    def __init__(self, *, artifact_type: ArtifactType) -> None:
        self.artifact_type = artifact_type
        """The artifact type to match."""

    def match(self, artifact: ArtifactModel) -> bool:
        return artifact.header.type == self.artifact_type


class AndFilter(ArtifactFilter):
    """A generic filter that implements a logical AND of filters."""

    def __init__(self, *filters: ArtifactFilter) -> None:
        self.filters = filters
        """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return all(filter.match(artifact) for filter in self.filters)


class OrFilter(ArtifactFilter):
    """A generic filter that implements a logical OR of filters."""

    def __init__(self, *filters: ArtifactFilter) -> None:
        self.filters = filters
        """The filters of which the composition is composed."""

    def match(self, artifact: ArtifactModel) -> bool:
        return any(filter.match(artifact) for filter in self.filters)


class AllFilter(ArtifactFilter):
    """A filter that matches all artifacts."""

    def __init__(self) -> None:
        pass

    def match(self, _: ArtifactModel) -> bool:
        return True


class NoneFilter(ArtifactFilter):
    """A filter that matches no artifacts."""

    def __init__(self) -> None:
        pass

    def match(self, _: ArtifactModel) -> bool:
        return False
