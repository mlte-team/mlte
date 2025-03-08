"""
Unit tests for specification model.
"""

from __future__ import annotations

from mlte.tests.model import TestSuiteModel
from test.fixture.artifact import make_complete_test_suite_model


def test_spec_body() -> None:
    """A TestSuite model can be serialized and deserialized."""
    objects = [
        make_complete_test_suite_model(),
        TestSuiteModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = TestSuiteModel.from_json(s)
        assert d == object
