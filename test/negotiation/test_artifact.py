"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

from __future__ import annotations

from typing import Tuple

import pytest

import mlte.store.error as errors
from mlte.context.context import Context
from mlte.negotiation.artifact import NegotiationCard
from mlte.store.artifact.store import ArtifactStore

from ..fixture.store import store  # noqa
from ..fixture.store import store_with_context  # noqa
from ..fixture.store import FX_MODEL_ID, FX_NAMESPACE_ID, FX_VERSION_ID  # noqa


def test_round_trip() -> None:
    """Negotiation card can be converted to model and back."""

    card = NegotiationCard("my-card")

    model = card.to_model()
    _ = NegotiationCard.from_model(model)


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Negotiation card can be saved to and loaded from artifact store."""
    store, ctx = store_with_context  # noqa

    card = NegotiationCard("my-card")
    card.save_with(ctx, store)

    loaded = NegotiationCard.load_with("my-card", context=ctx, store=store)
    assert loaded == card


def test_save_noparents(store: ArtifactStore) -> None:  # noqa
    """Save fails when no parents are present."""
    ctx = Context(FX_NAMESPACE_ID, FX_MODEL_ID, FX_VERSION_ID)

    card = NegotiationCard("my-card")
    with pytest.raises(errors.ErrorNotFound):
        card.save_with(ctx, store)


def test_save_parents(store: ArtifactStore) -> None:  # noqa
    """Save succeeds when parents are present."""
    ctx = Context(FX_NAMESPACE_ID, FX_MODEL_ID, FX_VERSION_ID)

    card = NegotiationCard("my-card")
    card.save_with(ctx, store, parents=True)


def test_save_overwrite(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Save succeeds when old artifact is overwritten."""
    store, ctx = store_with_context  # noqa

    # Initial write succeeds
    card = NegotiationCard("my-card")
    card.save_with(ctx, store)

    # Write without `force` fails
    with pytest.raises(errors.ErrorAlreadyExists):
        card.save_with(ctx, store)

    # Force write succeeds
    card.save_with(ctx, store, force=True)
