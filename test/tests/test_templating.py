"""Tests for template generation."""

from mlte.tests.templating import generate_suite_str
from test.negotiation.test_artifact import get_sample_negotiation_card

def test_generate_suite_str():
    """Test that the str generated is executable."""
    card = get_sample_negotiation_card()
    suite_str = generate_suite_str(card.quality_scenarios)
    exec(suite_str)
    assert True