"""
mlte/negotiation/artifact.py

Artifact implementation for negotiation card.
"""

from __future__ import annotations

import typing
from typing import List

from deepdiff import DeepDiff

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.model.shared import DataDescriptor, ModelDescriptor
from mlte.negotiation.model import NegotiationCardModel, SystemDescriptor

DEFAULT_NEGOTIATION_CARD_ID = "default.negotiation_card"


class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str = DEFAULT_NEGOTIATION_CARD_ID,
        system: SystemDescriptor = SystemDescriptor(),
        data: List[DataDescriptor] = [],
        model: ModelDescriptor = ModelDescriptor(),
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)

        self.system = system
        """A descriptor for the system into which the model is integrated."""

        self.data = data
        """A collection of descriptors for relevant datasets."""

        self.model = model
        """A descriptor for the model."""

    def to_model(self) -> ArtifactModel:
        """Convert a negotation card artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=NegotiationCardModel(
                system=self.system,
                data=self.data,
                model=self.model,
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> NegotiationCard:  # type: ignore[override]
        """Convert a negotiation card model to its corresponding artifact."""
        assert (
            model.header.type == ArtifactType.NEGOTIATION_CARD
        ), "Broken precondition."
        body = typing.cast(NegotiationCardModel, model.body)
        return NegotiationCard(
            identifier=model.header.identifier,
            system=body.system,
            data=body.data,
            model=body.model,
        )

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_NEGOTIATION_CARD_ID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NegotiationCard):
            return False
        return len(DeepDiff(self, other)) == 0
