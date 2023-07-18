"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

import mlte.negotiation.model as model
from mlte.artifact import Artifact, ArtifactType


class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str,
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)

        self.system: model.SystemDescriptor = model.SystemDescriptor()
        """A descriptor for the system into which the model is integrated."""

        self.data: list[model.DataDescriptor] = []
        """A collection of descriptors for relevant datasets."""

        self.model: model.ModelDescriptor = model.ModelDescriptor()
        """A descriptor for the model."""
