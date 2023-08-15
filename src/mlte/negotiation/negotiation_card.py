"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

import typing

import deepdiff

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel, ArtifactType
from mlte.context.context import Context
from mlte.negotiation.model import (
    DataDescriptor,
    ModelDescriptor,
    NegotiationCardModel,
    SystemDescriptor,
)
from mlte.store.store import ManagedSession, Store


class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str,
        system: SystemDescriptor = SystemDescriptor(),
        data: list[DataDescriptor] = [],
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
            header=ArtifactHeaderModel(
                identifier=self.identifier,
                type=self.type,
            ),
            body=NegotiationCardModel(
                system=self.system, data=self.data, model=self.model
            ),
        )

    @staticmethod
    def from_model(model: ArtifactModel) -> NegotiationCard:  # type: ignore[override]
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

    def save_with(self, context: Context, store: Store) -> None:
        """
        Save an artifact with the given context and store configuration.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        """
        with ManagedSession(store.session()) as handle:
            handle.write_artifact(
                context.namespace,
                context.model,
                context.version,
                self.to_model(),
            )

    @staticmethod
    def load_with(identifier: str, context: Context, store: Store) -> Artifact:
        """
        Load an artifact with the given context and store configuration.
        :param identifier: The identifier for the artifact
        :param context: The context from which to load the artifact
        :param store: The store from which to load the artifact
        """
        with ManagedSession(store.session()) as handle:
            return NegotiationCard.from_model(
                handle.read_artifact(
                    context.namespace,
                    context.model,
                    context.version,
                    identifier,
                )
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NegotiationCard):
            return False
        return (
            self.system == other.system
            and len(deepdiff.DeepDiff(self.data, other.data)) == 0
            and self.model == other.model
        )
