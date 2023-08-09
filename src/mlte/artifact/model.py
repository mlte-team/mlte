"""
mlte/artifact/model.py

Model implementation for MLTE artifacts.
"""

from enum import Enum

from mlte.model import BaseModel
from mlte.negotiation.model import NegotiationCardModel


class ArtifactType(str, Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = "negotiation_card"
    """The negotiation card artifact type."""


class ArtifactHeaderModel(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the artifact."""

    type: ArtifactType
    """The type identfier for the artifact."""


class ArtifactModel(BaseModel):
    """The base model for all MLTE artifacts."""

    header: ArtifactHeaderModel
    """The artifact header."""

    body: NegotiationCardModel
    """
    The artifact body.
    NOTE(Kyle): This will ultimately be a union over artifact types.
    Artifact polymorphism is achieved via this union. For now, only
    this single type is represented because it is the only artifact
    model that is currently implemented.
    """
