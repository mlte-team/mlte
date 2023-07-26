"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

from mlte.negotiation.negotiation_card import NegotiationCard


def test_round_trip() -> None:
    """Negotiation card can be converted to model and back."""

    card = NegotiationCard("my-card")

    model = card.to_model()
    _ = NegotiationCard.from_model(model)
