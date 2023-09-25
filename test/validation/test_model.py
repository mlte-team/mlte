"""
test/validation/test_model.py

Unit tests for validated specification model.
"""

from __future__ import annotations

import mlte.validation.model as model
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.spec.model import ConditionModel

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_validated_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        model.ValidatedSpecModel(
            artifact_type=ArtifactType.VALIDATED_SPEC,
            properties=[
                model.PropertyAndResultsModel(
                    name="TaskEfficacy",
                    description="Property for useful things.",
                    rationale="Because I say so",
                    module="mlte.properties.functionality.task_efficacy",
                    conditions={
                        "accuracy": ConditionModel(
                            name="less_than",
                            arguments=[3.0],
                            callback="invalid^#*@&^ASD@#",
                        )
                    },
                    results={
                        "accuracy": model.ResultModel(
                            type="Success",
                            message="The RF accuracy is greater than 3",
                            metadata=EvidenceMetadata(
                                measurement_type="ExternalMeasurement",
                                identifier=Identifier(name="accuracy"),
                                info="function: skleran.accu()",
                            ),
                        )
                    },
                )
            ],
        ),
        model.ValidatedSpecModel(artifact_type=ArtifactType.VALIDATED_SPEC),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ValidatedSpecModel.from_json(s)
        assert d == object
