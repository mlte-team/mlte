"""Tests for template generation."""

import ast

from mlte.suite.templating import generate_suite_str
from test.negotiation.test_artifact import get_sample_negotiation_card


def test_generate_suite_str():
    """Test that the str generated is valid code."""
    card = get_sample_negotiation_card()
    suite_str = generate_suite_str(card.quality_scenarios)
    ast.parse(suite_str)
