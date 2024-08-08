"""
test/model/test_shared.py

Unit tests for shared model components.
"""

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
    ModelInterfaceDescriptor,
    ModelIODescriptor,
    ModelProductionDescriptor,
    ModelResourcesDescriptor,
    RiskDescriptor,
)


def test_metric_descriptor() -> None:
    """A metric descriptor model can be serialized and deserialized."""
    m = MetricDescriptor(description="description", baseline="baseline")
    expected = {"description": "description", "baseline": "baseline"}
    assert deepequal(expected, m.to_json())

    objects = [
        MetricDescriptor(description="description", baseline="baseline"),
        MetricDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = MetricDescriptor.from_json(s)
        assert d == object


def test_goal_descriptor() -> None:
    """A goal descriptor model can be serialized and deserialized."""
    m = GoalDescriptor(
        description="description",
        metrics=[
            MetricDescriptor(description="description", baseline="baseline")
        ],
    )
    expected = {
        "description": "description",
        "metrics": [{"description": "description", "baseline": "baseline"}],
    }
    assert deepequal(expected, m.to_json())

    objects = [
        GoalDescriptor(
            description="description",
            metrics=[
                MetricDescriptor(description="description", baseline="baseline")
            ],
        ),
        GoalDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = GoalDescriptor.from_json(s)
        assert d == object


def test_risk_descriptor() -> None:
    """A risk descriptor model can be serialized and deserialized successfully."""
    objects = [
        RiskDescriptor(fp="fp", fn="fn", other="other"),
        RiskDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = RiskDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


def test_data_label_descriptor() -> None:
    """A data label descriptor model can be serialized and deserialized."""
    objects = [
        LabelDescriptor(
            name="label1", description="description", percentage=95.0
        ),
        LabelDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = LabelDescriptor.from_json(s)
        assert d == object


def test_data_field_descriptor() -> None:
    """A data field descriptor model can be serialized and deserialized."""
    objects = [
        FieldDescriptor(
            name="name",
            description="description",
            type="type",
            expected_values="expected_values",
            missing_values="missing_values",
            special_values="special_values",
        ),
        FieldDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = FieldDescriptor.from_json(s)
        assert d == object


def test_data_descriptor() -> None:
    """A data descriptor model can be serialized and deserialized."""

    objects = [
        DataDescriptor(
            description="description",
            classification=DataClassification.UNCLASSIFIED,
            access="access",
            labeling_method="by hand",
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
                    name="label1", description="description", percentage=95.0
                )
            ],
            policies="policies",
            rights="rights",
            source="source",
        ),
        DataDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = DataDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


def test_model_resources_descriptor() -> None:
    """A model resources descriptor model can be serialized and deserialized."""
    objects = [
        ModelResourcesDescriptor(
            cpu="cpu", gpu="gpu", memory="memory", storage="storage"
        ),
        ModelResourcesDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = ModelResourcesDescriptor.from_json(s)
        assert d == object


def test_model_input_descriptor() -> None:
    """A model input descriptor model can be serialized and deserialized."""
    objects = [
        ModelIODescriptor(description="description"),
        ModelIODescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = ModelIODescriptor.from_json(s)
        assert d == object


def test_model_interface_descriptor() -> None:
    """A model interface descriptor model can be serialized and deserialized."""
    objects = [
        ModelInterfaceDescriptor(
            inputs=[
                ModelIODescriptor(
                    name="i1", description="description", type="string"
                )
            ],
            outputs=[
                ModelIODescriptor(
                    name="o1", description="description", type="string"
                )
            ],
        ),
        ModelInterfaceDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = ModelInterfaceDescriptor.from_json(s)
        assert d == object


def test_model_development_descriptor() -> None:
    """A model development descriptor model can be serialized and deserialized."""
    objects = [
        ModelDevelopmentDescriptor(
            resources=ModelResourcesDescriptor(
                cpu="cpu", gpu="gpu", memory="memory", storage="storage"
            )
        ),
        ModelDevelopmentDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = ModelDevelopmentDescriptor.from_json(s)
        assert d == object


def test_model_production_descriptor() -> None:
    """A model production descriptor model can be serialized and deserialized."""
    objects = [
        ModelProductionDescriptor(
            deployment_platform="local server",
            capability_deployment_mechanism="API",
            interface=ModelInterfaceDescriptor(
                inputs=[
                    ModelIODescriptor(
                        name="i1", description="description", type="string"
                    )
                ],
                outputs=[
                    ModelIODescriptor(
                        name="o1", description="description", type="string"
                    )
                ],
            ),
            resources=ModelResourcesDescriptor(
                cpu="cpu", gpu="gpu", memory="memory", storage="storage"
            ),
        ),
        ModelProductionDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = ModelProductionDescriptor.from_json(s)
        assert d == object


def test_model_descriptor() -> None:
    """A model descriptor model can be serialized and deserialized."""
    objects = [
        ModelDescriptor(
            development=ModelDevelopmentDescriptor(
                resources=ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                )
            ),
            production=ModelProductionDescriptor(
                deployment_platform="local server",
                capability_deployment_mechanism="API",
                interface=ModelInterfaceDescriptor(
                    inputs=[
                        ModelIODescriptor(
                            name="i1", description="description", type="string"
                        )
                    ],
                    outputs=[
                        ModelIODescriptor(
                            name="o1", description="description", type="string"
                        )
                    ],
                ),
                resources=ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                ),
            ),
        ),
        ModelDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = ModelDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


def deepequal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return len(DeepDiff(a, b)) == 0
