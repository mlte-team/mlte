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
from mlte.negotiation.model import (
    DataDescriptor,
    ModelDescriptor,
    NegotiationCardDataModel,
    NegotiationCardModel,
    QASDescriptor,
    SystemDescriptor,
)
from mlte.store.artifact.store import ArtifactStore

DEFAULT_NEGOTIATION_CARD_ID = "default.negotiation_card"

QAS_ID_PREFIX = "qas_id_"


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

    # ----------------------------------------------------------------------------------
    # QAS methods.
    # ----------------------------------------------------------------------------------

    @staticmethod
    def build_qas_id(id_pos: int) -> str:
        """Returns a well formed id for a QAS, based on the prefix and position."""
        # Note we pad the number with up to 2 zeroes.
        return f"{QAS_ID_PREFIX}{id_pos:03d}"

    @staticmethod
    def get_pos_from_qas_id(qas_id: str) -> int:
        """Returns the position of the QAS id from its name."""
        return int(qas_id.replace(QAS_ID_PREFIX, ""))

    def add_qas_ids(self):
        """Ensures that all QAS in the NegotiationCard have an id, and assigns one to those who don't have it."""
        # Find the highest position that has been assigned a QAS id.
        highest_id_pos = 0
        sorted_qas: list[QASDescriptor] = sorted(
            [
                qas
                for qas in self.quality_scenarios
                if qas.identifier is not None
            ],
            key=lambda x: x.identifier,  # type: ignore
            reverse=True,
        )
        if len(sorted_qas) > 0:
            highest_id_pos = self.get_pos_from_qas_id(sorted_qas[0].identifier)  # type: ignore[arg-type]

        # Go over all QAS and assign ids to those that don't have them, based on the highest position found.
        for qas in self.quality_scenarios:
            if qas.identifier is None:
                highest_id_pos += 1
                qas.identifier = self.build_qas_id(highest_id_pos)

    # Overriden.
    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.pre_save_hook(). Ensures that QAS that done have ids are assigned them.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        # Add ids to QAS as needed.
        self.add_qas_ids()

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
        """Prints the scenarios in a user-friednly way."""
        for qas in self.quality_scenarios:
            prefix = f"{qas.identifier} ({qas.quality}): "
            scenario = f"{qas.stimulus} from {qas.source} while in {qas.environment}, {qas.response}, {qas.measure}"
            print(f"{prefix}{scenario.lower().capitalize()}")
