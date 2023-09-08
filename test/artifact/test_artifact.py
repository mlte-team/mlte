"""
test/artifact/test_artifact.py

Unit tests for MLTE artifact protocol implementation.
"""

from mlte.negotiation.negotiation_card import NegotiationCard
from mlte.session.state import set_context, set_store

from ..fixture.store import FX_MODEL_ID, FX_NAMESPACE_ID, FX_VERSION_ID


def test_save_load_session() -> None:
    """
    Artifacts can be saved  and loaded from global session.

    TODO(Kyle): Can we make this parametric over artifact types?
    """

    set_context(FX_NAMESPACE_ID, FX_MODEL_ID, FX_VERSION_ID)
    set_store("memory://")

    a = NegotiationCard("my-card")

    a.save(parents=True)
    _ = NegotiationCard.load("my-card")
