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
        system: model.SystemDescriptor = model.SystemDescriptor(),
        data: list[model.DataDescriptor] = [],
        model: model.ModelDescriptor = model.ModelDescriptor(),
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)

        self.system = system
        """A descriptor for the system into which the model is integrated."""

        self.data = data
        """A collection of descriptors for relevant datasets."""

        self.model = model
        """A descriptor for the model."""

    def to_model(self) -> model.NegotiationCardModel:
        """Convert a negotation card artifact to its corresponding model."""
        return model.NegotiationCardModel(
            header=model.NegotiationCardHeaderModel(
                identifier=self.identifier, type=self.type
            ),
            body=model.NegotiationCardBodyModel(
                system=self.system, data=self.data, model=self.model
            ),
        )

    @staticmethod
    def from_model(model: model.NegotiationCardModel) -> NegotiationCard:
        """Convert a negotiation card model to its corresponding artifact."""
        return NegotiationCard(
            identifier=model.header.identifier,
            system=model.body.system,
            data=model.body.data,
            model=model.body.model,
        )
