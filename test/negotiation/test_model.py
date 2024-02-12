"""
test/negotiation/test_model.py

Unit tests for negotiation card model.
"""

from __future__ import annotations

from typing import Any, Dict

from deepdiff import DeepDiff

from mlte.model.shared import (
    DataClassification,
    DataDescriptor,
    FieldDescriptor,
    GoalDescriptor,
    LabelDescriptor,
    MetricDescriptor,
    ModelDescriptor,
    ModelDevelopmentDescriptor,
    ModelInputDescriptor,
    ModelInterfaceDescriptor,
    ModelOutputDescriptor,
    ModelProductionDescriptor,
    ModelResourcesDescriptor,
    ProblemType,
    RiskDescriptor,
)
from mlte.negotiation.model import NegotiationCardModel, SystemDescriptor

# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


def test_negotiation_card() -> None:
    """A negotiation card model can be serialized and deserialized."""
    objects = [
        NegotiationCardModel(
            system=SystemDescriptor(
                goals=[
                    GoalDescriptor(
                        description="description",
                        metrics=[
                            MetricDescriptor(
                                description="description", baseline="baseline"
                            )
                        ],
                    )
                ],
                problem_type=ProblemType.CLASSIFICATION,
                task="task",
                usage_context="usage_context",
                risks=RiskDescriptor(fp="fp", fn="fn", other="other"),
            ),
            data=[
                DataDescriptor(
                    description="description",
                    classification=DataClassification.UNCLASSIFIED,
                    access="access",
                    fields=[
                        FieldDescriptor(
                            name="name",
                            description="description",
                            type="type",
                            expected_values="expected_values",
                            missing_values="missing_values",
                            special_values="special_values",
                        )
                    ],
                    labels=[
                        LabelDescriptor(
                            description="description", percentage=95.0
                        )
                    ],
                    policies="policies",
                    rights="rights",
                    source="source",
                    identifiable_information="identifiable_information",
                )
            ],
            model=ModelDescriptor(
                development=ModelDevelopmentDescriptor(
                    resources=ModelResourcesDescriptor(
                        cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                    )
                ),
                production=ModelProductionDescriptor(
                    integration="integration",
                    interface=ModelInterfaceDescriptor(
                        input=ModelInputDescriptor(description="description"),
                        output=ModelOutputDescriptor(description="description"),
                    ),
                    resources=ModelResourcesDescriptor(
                        cpu="cpu",
                        gpu="gpu",
                        memory="memory",
                        storage="storage",
                    ),
                ),
            ),
        ),
        NegotiationCardModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = NegotiationCardModel.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


def test_system_descriptor() -> None:
    """A system descriptor model can be serialized and deserialized."""
    objects = [
        SystemDescriptor(
            goals=[
                GoalDescriptor(
                    description="description",
                    metrics=[
                        MetricDescriptor(
                            description="description", baseline="baseline"
                        )
                    ],
                )
            ],
            problem_type=ProblemType.CLASSIFICATION,
            task="task",
            usage_context="usage_context",
            risks=RiskDescriptor(fp="fp", fn="fn", other="other"),
        ),
        SystemDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = SystemDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Test Helpers
# -----------------------------------------------------------------------------


def deepequal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return len(DeepDiff(a, b)) == 0
