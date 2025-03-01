"""
Unit tests for TestResults model.
"""

from __future__ import annotations

import mlte.validation.model as model
from test.fixture.artifact import make_complete_test_results_model


def test_validated_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        make_complete_test_results_model(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.TestResultsModel.from_json(s)
        assert d == object
