"""
test/schema/test_report_schema.py

Unit tests for report schema validation.
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
from mlte.report.artifact import Report
from mlte.report.model import (
    CommentDescriptor,
    IntendedUseDescriptor,
    PerformanceDesciptor,
    QuantitiveAnalysisDescriptor,
    SummaryDescriptor,
)

from . import util as util


def test_empty_instance() -> None:
    """An empty instance validates successfully."""
    report = Report()

    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])


def test_valid_instance() -> None:
    """A complete instance validates successfully."""
    report = Report(
        "my-report",
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
                    LabelDescriptor(description="description", percentage=95.0)
                ],
                policies="policies",
                rights="rights",
                source="source",
            )
        ],
        comments=[CommentDescriptor(content="content")],
        quantitative_analysis=QuantitiveAnalysisDescriptor(content="content"),
    )
    doc = report.to_model().to_json()
    util.validate_report_schema(doc["body"])
