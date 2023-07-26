"""
mlte/artifact/artifact.py

Artifact protocol implementation.
"""

from __future__ import annotations

from enum import Enum

from mlte.model import BaseModel


class ArtifactType(str, Enum):
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
        self.identifier = identifier
        """
        The identifier for the artifact.
        An artifact identifier is unique within a MLTE context
        (namespace, model, version) and for a given artifact type.
        """

        self.type = type
        """The identifier for the artifact type"""

    def to_model(self) -> BaseModel:
        """Serialize an artifact to its corresponding model."""
        raise NotImplementedError(
            "Artifact.to_model() not implemented for abstract Artifact."
        )

    @staticmethod
    def from_model(_: BaseModel) -> Artifact:
        """Deserialize an artifact from its corresponding model."""
        raise NotImplementedError(
            "Artifact.from_model() not implemented for abstract Artifact."
        )
