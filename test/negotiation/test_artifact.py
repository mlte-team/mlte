"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

from __future__ import annotations

from typing import Tuple

import pytest

import mlte.store.error as errors
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.negotiation import qas
from mlte.negotiation.artifact import NegotiationCard
from mlte.negotiation.model import DataDescriptor
from mlte.negotiation.qas import QASDescriptor
from mlte.store.artifact.store import ArtifactStore
from test.fixture.artifact import ArtifactModelFactory
from test.store.artifact.fixture import (  # noqa
    FX_MODEL_ID,
    FX_VERSION_ID,
    memory_store,
    store_with_context,
)


def get_sample_negotiation_card(id: str = "my-card"):
    card_model = ArtifactModelFactory.make(ArtifactType.NEGOTIATION_CARD, id)
    return NegotiationCard.from_model(card_model)


def test_round_trip() -> None:
    """Negotiation card can be converted to model and back."""

    card = get_sample_negotiation_card()

    model = card.to_model()
    _ = NegotiationCard.from_model(model)


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Negotiation card can be saved to and loaded from artifact store."""
    store, ctx = store_with_context  # noqa

    card = get_sample_negotiation_card()
    card.save_with(ctx, store)

    loaded = NegotiationCard.load_with("my-card", context=ctx, store=store)
    assert loaded == card


def test_save_noparents(memory_store: ArtifactStore) -> None:  # noqa
    """Save fails when no parents are present."""
    ctx = Context(FX_MODEL_ID, FX_VERSION_ID)

    card = get_sample_negotiation_card()
    with pytest.raises(errors.ErrorNotFound):
        card.save_with(ctx, memory_store)


def test_save_parents(memory_store: ArtifactStore) -> None:  # noqa
    """Save succeeds when parents are present."""
    ctx = Context(FX_MODEL_ID, FX_VERSION_ID)

    card = get_sample_negotiation_card()
    card.save_with(ctx, memory_store, parents=True)


def test_save_overwrite(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Save succeeds when old artifact is overwritten."""
    store, ctx = store_with_context  # noqa

    # Initial write succeeds
    card = get_sample_negotiation_card()
    card.save_with(ctx, store)

    # Change card.
    card.data.append(DataDescriptor(description="New data descriptor"))

    # Write without `force` fails
    with pytest.raises(errors.ErrorAlreadyExists):
        card.save_with(ctx, store)

    # Force write succeeds
    read_card_model = card.save_with(ctx, store, force=True)
    read_card = NegotiationCard.from_model(read_card_model)
    assert card == read_card


def test_qas_id_generation():
    # Generate a sample negotiation card, with QAS without ids.
    card = get_sample_negotiation_card()
    card.quality_scenarios.append(
        QASDescriptor(quality="security", stimulus="test")
    )
    card.quality_scenarios.append(
        QASDescriptor(quality="performance", stimulus="test")
    )

    # Add new ids as needed.
    qas.add_qas_ids(card.identifier, card.quality_scenarios)

    for scenario in card.quality_scenarios:
        assert scenario.identifier is not None


def test_qas_id_increase():
    # Generate a sample negotiation card, with some QAS with id, and three others without.
    card = get_sample_negotiation_card()
    card.quality_scenarios = []
    card.quality_scenarios.append(
        QASDescriptor(quality="resilience", stimulus="test")
    )
    card.quality_scenarios.append(
        QASDescriptor(
            identifier=qas._build_qas_id(card.identifier, 1),
            quality="security",
            stimulus="test",
        )
    )
    card.quality_scenarios.append(
        QASDescriptor(quality="robustness", stimulus="test")
    )
    card.quality_scenarios.append(
        QASDescriptor(
            identifier=qas._build_qas_id(card.identifier, 2),
            quality="maintainability",
            stimulus="test",
        )
    )
    card.quality_scenarios.append(
        QASDescriptor(quality="perforemance", stimulus="test")
    )

    # Add ids as needed.
    qas.add_qas_ids(card.identifier, card.quality_scenarios)

    assert len(card.quality_scenarios) == 5
    assert card.quality_scenarios[0].identifier == qas._build_qas_id(
        card.identifier, 3
    )
    assert card.quality_scenarios[1].identifier == qas._build_qas_id(
        card.identifier, 1
    )
    assert card.quality_scenarios[2].identifier == qas._build_qas_id(
        card.identifier, 4
    )
    assert card.quality_scenarios[3].identifier == qas._build_qas_id(
        card.identifier, 2
    )
    assert card.quality_scenarios[4].identifier == qas._build_qas_id(
        card.identifier, 5
    )
