"""
test/spec/test_model.py

Unit tests for specification model.
"""

from __future__ import annotations

import mlte.spec.model as model
from mlte.artifact.type import ArtifactType

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        model.SpecModel(
            artifact_type=ArtifactType.SPEC,
            properties=[
                model.PropertyModel(
                    name="TaskEfficacy",
                    description="Property for useful things.",
                    rationale="Because I say so",
                    conditions={
                        "accuracy": model.ConditionModel(
                            name="less_than",
                            arguments=[3.0],
                            callback="invalid^#*@&^ASD@#",
                        )
                    },
                )
            ],
        ),
        model.SpecModel(artifact_type=ArtifactType.SPEC),
    ]

    for object in objects:
        s = object.to_json()
        d = model.SpecModel.from_json(s)
        assert d == object
