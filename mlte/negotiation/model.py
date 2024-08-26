"""
mlte/negotiation/model.py

Model implementation for negotiation card artifact.
"""

from __future__ import annotations

from typing import Literal

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.model.shared import NegotiationCardDataModel

# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


class NegotiationCardModel(BaseModel):
    """The model implementation for the NegotiationCard artifact."""

    artifact_type: Literal[
        ArtifactType.NEGOTIATION_CARD
    ] = ArtifactType.NEGOTIATION_CARD

    """Union discriminator."""

    nc_data: NegotiationCardDataModel = NegotiationCardDataModel()
    """The specific data for this negotiation card."""
