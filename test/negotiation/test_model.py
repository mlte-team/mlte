"""
test/negotiation/test_model.py

Unit tests for negotiation card model.
"""

from typing import Any

from deepdiff import DeepDiff

import mlte.negotiation.model as model

# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


def test_negotiation_card_body() -> None:
    """A negotiation card model can be serialized and deserialized."""
    objects = [
        model.NegotiationCardModel(
            system=model.SystemDescriptor(
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
            data=[
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
                )
            ],
            model=model.ModelDescriptor(
                development=model.ModelDevelopmentDescriptor(
                    resources=model.ModelResourcesDescriptor(
                        cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                    )
                ),
                production=model.ModelProductionDescriptor(
                    integration="integration",
                    interface=model.ModelInterfaceDescriptor(
                        input=model.ModelInputDescriptor(
                            description="description"
                        ),
                        output=model.ModelOutputDescriptor(
                            description="description"
                        ),
                    ),
                    resources=model.ModelResourcesDescriptor(
                        cpu="cpu",
                        gpu="gpu",
                        memory="memory",
                        storage="storage",
                    ),
                ),
            ),
        ),
        model.NegotiationCardModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.NegotiationCardModel.from_json(s)
        assert d == object


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
    m = model.GoalDescriptor(
        description="description",
        metrics=[
            model.MetricDescriptor(
                description="description", baseline="baseline"
            )
        ],
    )
    expected = {
        "description": "description",
        "metrics": [{"description": "description", "baseline": "baseline"}],
    }
    assert deepequal(expected, m.to_json())

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


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


def test_model_resources_descriptor() -> None:
    """A model resources descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelResourcesDescriptor(
            cpu="cpu", gpu="gpu", memory="memory", storage="storage"
        ),
        model.ModelResourcesDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ModelResourcesDescriptor.from_json(s)
        assert d == object


def test_model_input_descriptor() -> None:
    """A model input descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelInputDescriptor(description="description"),
        model.ModelInputDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ModelInputDescriptor.from_json(s)
        assert d == object


def test_model_output_descriptor() -> None:
    """A model output descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelOutputDescriptor(description="description"),
        model.ModelOutputDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ModelOutputDescriptor.from_json(s)
        assert d == object


def test_model_interface_descriptor() -> None:
    """A model interface descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelInterfaceDescriptor(
            input=model.ModelInputDescriptor(description="description"),
            output=model.ModelOutputDescriptor(description="description"),
        ),
        model.ModelInterfaceDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.ModelInterfaceDescriptor.from_json(s)
        assert d == object


def test_model_development_descriptor() -> None:
    """A model development descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelDevelopmentDescriptor(
            resources=model.ModelResourcesDescriptor(
                cpu="cpu", gpu="gpu", memory="memory", storage="storage"
            )
        ),
        model.ModelDevelopmentDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = model.ModelDevelopmentDescriptor.from_json(s)
        assert d == object


def test_model_production_descriptor() -> None:
    """A model production descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelProductionDescriptor(
            integration="integration",
            interface=model.ModelInterfaceDescriptor(
                input=model.ModelInputDescriptor(description="description"),
                output=model.ModelOutputDescriptor(description="description"),
            ),
            resources=model.ModelResourcesDescriptor(
                cpu="cpu", gpu="gpu", memory="memory", storage="storage"
            ),
        ),
        model.ModelProductionDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ModelProductionDescriptor.from_json(s)
        assert d == object


def test_model_descriptor() -> None:
    """A model descriptor model can be serialized and deserialized."""
    objects = [
        model.ModelDescriptor(
            development=model.ModelDevelopmentDescriptor(
                resources=model.ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                )
            ),
            production=model.ModelProductionDescriptor(
                integration="integration",
                interface=model.ModelInterfaceDescriptor(
                    input=model.ModelInputDescriptor(description="description"),
                    output=model.ModelOutputDescriptor(
                        description="description"
                    ),
                ),
                resources=model.ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                ),
            ),
        ),
        model.ModelDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = model.ModelDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Test Helpers
# -----------------------------------------------------------------------------


def deepequal(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return len(DeepDiff(a, b)) == 0
