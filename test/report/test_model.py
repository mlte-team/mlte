"""
test/report/test_model.py

Unit tests for report model.
"""

from mlte.model.shared import (
    GoalDescriptor,
    MetricDescriptor,
    ModelInputDescriptor,
    ModelInterfaceDescriptor,
    ModelOutputDescriptor,
    ModelProductionDescriptor,
    ModelResourcesDescriptor,
    ProblemType,
)
from mlte.report.model import (
    CommentDescriptor,
    IntendedUseDescriptor,
    PerformanceDesciptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
    SummaryDescriptor,
)
from test.fixture.artifact import make_complete_report


def test_report() -> None:
    """A report model can be serialized and deserialized."""
    objects = [
        make_complete_report(),
        ReportModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = ReportModel.from_json(s)
        assert d == object


def test_summary() -> None:
    """A summary descriptor can be serialized and deserialized."""
    objects = [
        SummaryDescriptor(problem_type=ProblemType.CLASSIFICATION, task="task"),
        SummaryDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = SummaryDescriptor.from_json(s)
        assert d == object


def test_performance() -> None:
    """A performance descriptor can be serialized and deserialized."""
    objects = [
        PerformanceDesciptor(
            goals=[
                GoalDescriptor(
                    description="description",
                    metrics=[
                        MetricDescriptor(
                            description="description", baseline="baseline"
                        )
                    ],
                )
            ]
        ),
        PerformanceDesciptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = PerformanceDesciptor.from_json(s)
        assert d == object


def test_intended_use() -> None:
    """An intended use descriptor can be serialized and deserialized."""
    objects = [
        IntendedUseDescriptor(
            usage_context="context",
            production_requirements=ModelProductionDescriptor(
                deployment_platform="local server",
                capability_deployment_mechanism="API",
                interface=ModelInterfaceDescriptor(
                    input=ModelInputDescriptor(description="description"),
                    output=ModelOutputDescriptor(description="output"),
                ),
                resources=ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                ),
            ),
        ),
        IntendedUseDescriptor(),
    ]

    for object in objects:
        s = object.to_json()
        d = IntendedUseDescriptor.from_json(s)
        assert d == object


def test_comment() -> None:
    """A comment can be serialized and deserialized."""
    objects = [
        CommentDescriptor(content="content"),
    ]

    for object in objects:
        s = object.to_json()
        d = CommentDescriptor.from_json(s)
        assert d == object


def test_quantitative_analysis() -> None:
    """A quantitative analysis model can be serialized and deserialized."""
    objects = [
        QuantitiveAnalysisDescriptor(content="content"),
        QuantitiveAnalysisDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = QuantitiveAnalysisDescriptor.from_json(s)
        assert d == object
