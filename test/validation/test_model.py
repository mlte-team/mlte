"""
test/validation/test_model.py

Unit tests for validated specification model.
"""

from __future__ import annotations

import typing

import mlte.validation.model as model
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.property.functionality.task_efficacy import TaskEfficacy
from mlte.spec.condition import Condition
from mlte.spec.model import SpecModel
from mlte.spec.spec import Spec

# -----------------------------------------------------------------------------
# SpecModel
# -----------------------------------------------------------------------------


def test_validated_spec_body() -> None:
    """A spec model can be serialized and deserialized."""
    objects = [
        model.ValidatedSpecModel(
            spec_identifier="Spec1",
            spec=typing.cast(
                SpecModel,
                Spec(
                    "Spec1",
                    properties={
                        TaskEfficacy("rat"): {
                            "accuracy": Condition(
                                name="less_than",
                                arguments=[3.0],
                                callback="invalid^#*@&^ASD@#",
                                value_class="mlte.value.types.real.Real",
                            )
                        }
                    },
                )
                .to_model()
                .body,
            ),
            results={
                "TaskEfficacy": {
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
            },
        ),
        model.ValidatedSpecModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ValidatedSpecModel.from_json(s)
        assert d == object
