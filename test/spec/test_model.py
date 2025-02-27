"""
test/spec/test_model.py

Unit tests for specification model.
"""

from __future__ import annotations

from mlte.spec.model import TestSuiteModel
from test.fixture.artifact import make_complete_spec_model

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        make_complete_spec_model(),
        TestSuiteModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = TestSuiteModel.from_json(s)
        assert d == object
