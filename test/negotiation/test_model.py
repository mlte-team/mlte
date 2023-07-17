"""
test/negotiation/test_model.py

Unit tests for negotiation card model.
"""

from typing import Any

from deepdiff import DeepDiff

import mlte.negotiation.model as model


def deepequal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return len(DeepDiff(a, b)) == 0


# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


def test_metric_descriptor() -> None:
    """A metric descriptor model can be serialized and deserialized."""
    m = model.MetricDescriptor(description="description", baseline="baseline")
    expected = {"description": "description", "baseline": "baseline"}
    assert deepequal(expected, m.to_json())

    objects = [
        model.MetricDescriptor(description="description", baseline="baseline"),
        model.MetricDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.MetricDescriptor.from_json(s)
        assert d == object


def test_goal_descriptor() -> None:
    """A goal descriptor model can be serialized and deserialized."""
    objects = [
        model.GoalDescriptor(
            description="description",
            metrics=[
                model.MetricDescriptor(
                    description="description", baseline="baseline"
                )
            ],
        ),
        model.GoalDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.GoalDescriptor.from_json(s)
        assert d == object


def test_risk_descriptor() -> None:
    """A risk descriptor model can be serialized and deserialized successfully."""
    objects = [
        model.RiskDescriptor(fp="fp", fn="fn", other="other"),
        model.RiskDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.RiskDescriptor.from_json(s)
        assert d == object


def test_system_descriptor() -> None:
    """A system descriptor model can be serialized and deserialized."""
    objects = [
        model.SystemDescriptor(
            goals=[
                model.GoalDescriptor(
                    description="description",
                    metrics=[
                        model.MetricDescriptor(
                            description="description", baseline="baseline"
                        )
                    ],
                )
            ],
            problem_type=model.ProblemType.CLASSIFICATION,
            task="task",
            usage_context="usage_context",
            risks=model.RiskDescriptor(fp="fp", fn="fn", other="other"),
        ),
        model.SystemDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.SystemDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


def test_data_label_descriptor() -> None:
    """A data label descriptor model can be serialized and deserialized."""
    objects = [
        model.LabelDescriptor(description="description", percentage=95.0),
        model.LabelDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.LabelDescriptor.from_json(s)
        assert d == object


def test_data_field_descriptor() -> None:
    """A data field descriptor model can be serialized and deserialized."""
    objects = [
        model.FieldDescriptor(
            name="name",
            description="description",
            type="type",
            expected_values="expected_values",
            missing_values="missing_values",
            special_values="special_values",
        ),
        model.FieldDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.FieldDescriptor.from_json(s)
        assert d == object


def test_data_descriptor() -> None:
    """A data descriptor model can be serialized and deserialized."""

    objects = [
        model.DataDescriptor(
            description="description",
            classification=model.DataClassification.UNCLASSIFIED,
            access="access",
            fields=[
                model.FieldDescriptor(
                    name="name",
                    description="description",
                    type="type",
                    expected_values="expected_values",
                    missing_values="missing_values",
                    special_values="special_values",
                )
            ],
            labels=[
                model.LabelDescriptor(
                    description="description", percentage=95.0
                )
            ],
            policies="policies",
            rights="rights",
            source="source",
            identifiable_information="identifiable_information",
        ),
        model.DataDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.DataDescriptor.from_json(s)
        assert d == object
