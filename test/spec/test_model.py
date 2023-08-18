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
            metadata=model.SpecMetadataModel(
                namespace="ns0", model="model0", version="0.0.1", timestamp=1000
            ),
            properties=[
                model.PropertyModel(
                    name="TaskEfficacy",
                    repr="TaskEfficacy()",
                    description="Property for useful things.",
                    rationale="Because I say so",
                    conditions=[
                        model.ConditionModel(
                            name="less_than",
                            arguments=[3.0],
                            callback="invalid^#*@&^ASD@#",
                        )
                    ],
                )
            ],
        ),
        model.SpecModel(
            artifact_type=ArtifactType.SPEC, metadata=model.SpecMetadataModel()
        ),
    ]

    for object in objects:
        s = object.to_json()
        d = model.SpecModel.from_json(s)
        assert d == object
