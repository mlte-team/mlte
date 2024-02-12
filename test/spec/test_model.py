"""
test/spec/test_model.py

Unit tests for specification model.
"""

from __future__ import annotations

import mlte.spec.model as model

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        model.SpecModel(
            properties=[
                model.PropertyModel(
                    name="TaskEfficacy",
                    description="Property for useful things.",
                    rationale="Because I say so",
                    module="mlte.properties.functionality.task_efficacy",
                    conditions={
                        "accuracy": model.ConditionModel(
                            name="less_than",
                            arguments=[3.0],
                            callback="invalid^#*@&^ASD@#",
                            value_class="mlte.value.types.real.Real",
                        )
                    },
                )
            ],
        ),
        model.SpecModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.SpecModel.from_json(s)
        assert d == object
