"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from mlte.artifact.model import BaseModel


class ArtifactType(Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = "negotiation_card"
    """The negotiation card artifact type."""


class Artifact:
    """
    The MLTE artifact protocol implementation.

    The Artifact type establishes the common interface
    for all MLTE artifacts. This ensures that, even though
    they have very different semantics, all artifacts abide
    by a common protocol that allows us to perform common
    operations with them, namely persistence.
    """

    def __init__(self, identifier: str, type: ArtifactType) -> None:
        # Context data must be populated prior to artifact construction

        self.header = (
            ArtifactHeader.builder().with_identifier(identifier).build()
        )
        """The common artifact header."""

    def model(self) -> BaseModel:
        """Return the corresponding model for an artifact."""
        raise NotImplementedError(
            "Artifact.model() not implemented for abstract Artifact."
        )


@dataclass
class ArtifactHeader:
    """
    A common header for all MLTE artifacts.

    We distinguish between the artifact "metadata" and the
    artifact "header" because the metadata merely encodes all
    of the contextual information, whereas the header maintains
    data that is still consistent across artifacts, but is not
    derived from the MLTE context in which it is constructed.
    """

    identifier: str
    """The unique identifier for the artifact."""

    type: ArtifactType
    """The type identifier for the artifact"""

    @staticmethod
    def builder() -> ArtifactHeaderBuilder:
        """
        Get a builder for ArtifactHeader.
        :return: The builder instance
        """
        return ArtifactHeaderBuilder()


class ArtifactHeaderBuilder:
    """A builder for artifact headers."""

    def __init__(self) -> None:
        self._identifier: Optional[str] = None
        """The unique idenifier for the artifact."""

        self._type: Optional[ArtifactType] = None
        """The type identifier for the artifact."""

    def with_identifier(self, identifier: str) -> ArtifactHeaderBuilder:
        """
        Attach the artifact identifier to artifact header.
        :param model: The artifact identifier
        :return: The builder
        """
        self._identifier = identifier
        return self

    def with_type(self, type: ArtifactType) -> ArtifactHeaderBuilder:
        """
        Attach the artifact type identifier to artifact header.
        :param model: The artifact type
        :return: The builder
        """
        self._type = type
        return self

    def build(self) -> ArtifactHeader:
        """
        Finalize the builder.
        :return: The artifact header instance
        """
        if self._identifier is None:
            raise ValueError("ArtifactHeader must specify identifier.")
        if self._type is None:
            raise ValueError("ArtifactHeader must specify type.")
        return ArtifactHeader(identifier=self._identifier, type=self._type)
