"""
mlte/artifact/model.py

Model implementation for MLTE artifacts.
"""

from enum import Enum, auto
from typing import Union

from mlte.model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.value.model import ValueModel


class ArtifactType(str, Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = auto()
    """The negotiation card artifact type."""

    VALUE = auto()
    """The value card artifact type."""


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

    body: Union[NegotiationCardModel, ValueModel]
    """The artifact body."""
