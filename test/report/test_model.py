"""
test/report/test_model.py

Unit tests for report model.
"""

from mlte.model.shared import (
    DataClassification,
    DataDescriptor,
    FieldDescriptor,
    GoalDescriptor,
    LabelDescriptor,
    MetricDescriptor,
    ModelInputDescriptor,
    ModelInterfaceDescriptor,
    ModelOutputDescriptor,
    ModelProductionDescriptor,
    ModelResourcesDescriptor,
    ProblemType,
    RiskDescriptor,
)
from mlte.report.model import (
    CommentDescriptor,
    IntendedUseDescriptor,
    PerformanceDesciptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
    SummaryDescriptor,
)


def test_report() -> None:
    """A report model can be serialized and deserialized."""
    objects = [
        ReportModel(
            summary=SummaryDescriptor(
                problem_type=ProblemType.CLASSIFICATION, task="task"
            ),
            performance=PerformanceDesciptor(
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
            intended_use=IntendedUseDescriptor(
                usage_context="context",
                production_requirements=ModelProductionDescriptor(
                    integration="integration",
                    interface=ModelInterfaceDescriptor(
                        input=ModelInputDescriptor(description="description"),
                        output=ModelOutputDescriptor(description="output"),
                    ),
                    resources=ModelResourcesDescriptor(
                        cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                    ),
                ),
            ),
            risks=RiskDescriptor(fp="fp", fn="fn", other="other"),
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
            comments=[CommentDescriptor(content="content")],
            quantitative_analysis=QuantitiveAnalysisDescriptor(
                content="content"
            ),
        ),
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
                integration="integration",
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
