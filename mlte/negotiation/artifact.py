"""
mlte/negotiation/artifact.py

Artifact implementation for negotiation card.
"""

from __future__ import annotations

import typing
from typing import List, Optional

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.base_model import BaseModel
from mlte.negotiation import qas
from mlte.negotiation.model import (
    DataDescriptor,
    ModelDescriptor,
    NegotiationCardDataModel,
    NegotiationCardModel,
    SystemDescriptor,
)
from mlte.negotiation.qas import QASDescriptor
from mlte.store.artifact.store import ArtifactStore

DEFAULT_NEGOTIATION_CARD_ID = "default.negotiation_card"


class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str = DEFAULT_NEGOTIATION_CARD_ID,
        system: SystemDescriptor = SystemDescriptor(),
        data: List[DataDescriptor] = [],
        model: ModelDescriptor = ModelDescriptor(),
        quality_scenarios: List[QASDescriptor] = [],
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)

        self.system = system
        """A descriptor for the system into which the model is integrated."""

        self.data = data
        """A collection of descriptors for relevant datasets."""

        self.model = model
        """A descriptor for the model."""

        self.quality_scenarios = quality_scenarios
        """A list of quality attribute scenarios."""

    # ----------------------------------------------------------------------------------
    # Serialization methods.
    # ----------------------------------------------------------------------------------
    # Overriden.
    def to_model(self) -> ArtifactModel:
        """Convert a negotation card artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=NegotiationCardModel(
                nc_data=NegotiationCardDataModel(
                    system=self.system,
                    data=self.data,
                    model=self.model,
                    system_requirements=self.quality_scenarios,
                ),
            ),
        )

    # Overriden.
    @classmethod
    def from_model(cls, model: BaseModel) -> NegotiationCard:
        """Convert a negotiation card model to its corresponding artifact."""
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.NEGOTIATION_CARD
        ), "Type should be NegotiationCard."
        body = typing.cast(NegotiationCardModel, model.body)
        return NegotiationCard(
            identifier=model.header.identifier,
            system=body.nc_data.system,
            data=body.nc_data.data,
            model=body.nc_data.model,
            quality_scenarios=body.nc_data.system_requirements,
        )

    # Overriden.
    @classmethod
    def load(cls, identifier: Optional[str] = None) -> NegotiationCard:
        """
        Load a NegotiationCard from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.
        """
        card = super().load(identifier)
        return typing.cast(NegotiationCard, card)

    # Overriden.
    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.pre_save_hook(). Ensures that QAS that done have ids are assigned them.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        # Add ids to QAS as needed.
        qas.add_qas_ids(self.identifier, self.quality_scenarios)

    # ----------------------------------------------------------------------------------
    # Helper methods.
    # ----------------------------------------------------------------------------------

    # Overriden.
    @staticmethod
    def get_default_id() -> str:
        return DEFAULT_NEGOTIATION_CARD_ID

    # Overriden.
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NegotiationCard):
            return False
        return self._equal(other)

    def print_quality_scenarios(self):
        """Prints the scenarios in a user-friendly way."""
        for scenario in self.quality_scenarios:
            prefix = f"{scenario.identifier} ({scenario.quality}): "
            description = f"{scenario.stimulus} from {scenario.source} while in {scenario.environment}, {scenario.response}, {scenario.measure}"
            print(f"{prefix}{description.lower().capitalize()}")
