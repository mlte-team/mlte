"""
test/validation/test_model.py

Unit tests for validated specification model.
"""

from __future__ import annotations

from test.fixture.artifact import make_complete_validated_spec_model

import mlte.validation.model as model

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_validated_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        make_complete_validated_spec_model(),
        model.ValidatedSpecModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ValidatedSpecModel.from_json(s)
        assert d == object
