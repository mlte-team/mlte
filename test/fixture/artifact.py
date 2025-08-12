"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

from __future__ import annotations

import random
import string
import typing
from typing import List, Optional, Union

from mlte._private import meta
from mlte.artifact.factory import ArtifactFactory
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.model import EvidenceModel, IntegerValueModel
from mlte.evidence.types.integer import Integer
from mlte.measurement.model import MeasurementMetadata
from mlte.negotiation.model import (
    DataClassification,
    DataDescriptor,
    FieldDescriptor,
    GoalDescriptor,
    LabelDescriptor,
    MetricDescriptor,
    ModelDescriptor,
    ModelIODescriptor,
    ModelResourcesDescriptor,
    NegotiationCardModel,
    ProblemType,
    RiskDescriptor,
    SystemDescriptor,
)
from mlte.negotiation.qas import QASDescriptor
from mlte.report.model import CommentDescriptor, ReportModel
from mlte.results.model import ResultModel, TestResultsModel
from mlte.tests.model import TestCaseModel, TestSuiteModel
from mlte.tests.test_suite import TestSuite
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata


def _random_id(length: int = 5) -> str:
    """
    Generate a random identifier.
    :param length: The length of the ID
    :return: The identifier
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


class TypeUtil:
    """A static class for artifact type utilities."""

    @staticmethod
    def all_others(type: ArtifactType) -> List[ArtifactType]:
        """
        Return a collection of all artifact types that are not the given one.
        :param type: The excluded type
        :return: The included types
        """
        return [t for t in ArtifactType if t != type]


class ArtifactModelFactory:
    """A class for build artifacts."""

    @staticmethod
    def make(
        type: ArtifactType,
        id: str = _random_id(),
        user: Optional[str] = None,
    ) -> ArtifactModel:
        """
        Construct an artifact model of the given type.
        :param type: The artifact type
        :param id: The artifact identifier (default: randomly generated)
        :return: The artifact model
        """
        header = ArtifactHeaderModel(identifier=id, type=type, creator=user)

        body_model: Union[
            NegotiationCardModel,
            EvidenceModel,
            TestSuiteModel,
            TestResultsModel,
            ReportModel,
        ]
        if type == ArtifactType.NEGOTIATION_CARD:
            body_model = _make_negotiation_card()
        elif type == ArtifactType.EVIDENCE:
            body_model = _make_evidence(id)
        elif type == ArtifactType.TEST_SUITE:
            body_model = _make_test_suite()
        elif type == ArtifactType.TEST_RESULTS:
            body_model = _make_test_results()
        elif type == ArtifactType.REPORT:
            body_model = _make_report()
        else:
            raise RuntimeError(
                f"Unkown artifact type provided when creating body: {type}."
            )

        artifact = ArtifactFactory.from_model(
            ArtifactModel(header=header, body=body_model)
        )
        return typing.cast(ArtifactModel, artifact.to_model())


def _make_negotiation_card() -> NegotiationCardModel:
    """
    Make a simple negotiation card.
    :return: The artifact
    """
    return NegotiationCardModel(
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
            risks=RiskDescriptor(fp="fp", fn="fn", other=["other1", "other2"]),
        ),
        data=[
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
                        name="label1",
                        description="description",
                        percentage=95.0,
                    )
                ],
                policies="policies",
                rights="rights",
                source="source",
            )
        ],
        model=ModelDescriptor(
            development_compute_resources=ModelResourcesDescriptor(
                cpu="1",
                gpu="2",
                memory="600",
                storage="50",
            ),
            deployment_platform="local server",
            capability_deployment_mechanism="API",
            input_specification=[
                ModelIODescriptor(
                    name="i1",
                    description="description",
                    type="string",
                    expected_values="2, 4.5",
                )
            ],
            output_specification=[
                ModelIODescriptor(
                    name="o1",
                    description="description",
                    type="string",
                    expected_values="hi, bye",
                )
            ],
            production_compute_resources=ModelResourcesDescriptor(
                cpu="1",
                gpu="1",
                memory="600",
                storage="50",
            ),
        ),
        system_requirements=[
            QASDescriptor(
                quality="fairness",
                stimulus="new data arrives",
                source="from new area",
                environment="normal time",
                response="results are fair",
                measure="less than 1 percent difference",
            ),
            QASDescriptor(
                quality="fairness",
                stimulus="new data arrives",
                source="from new area",
                environment="normal time",
                response="results are fair",
                measure="less than 1 percent difference",
            ),
        ],
    )


def _make_evidence(id: str) -> EvidenceModel:
    """
    Make an evidence artifact.
    :return: The artifact
    """
    m = get_sample_evidence_metadata(test_case_id=id)

    return EvidenceModel(
        metadata=m,
        evidence_class=meta.get_qualified_name(Integer),
        value=IntegerValueModel(integer=1),
    )


def _make_test_suite() -> TestSuiteModel:
    """
    Make a minimal test suite.
    :return: The artifact
    """
    return TestSuiteModel(
        test_cases=[
            TestCaseModel(
                identifier="Test1",
                goal="QACategory for useful things.",
                validator=Validator(
                    bool_exp=lambda x: x.value < 3, success="Yay", failure="oh"
                ).to_model(),
                measurement=MeasurementMetadata(
                    measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
                    output_class="mlte.evidence.types.real.Real",
                ),
            )
        ],
    )


def _make_test_results() -> TestResultsModel:
    """
    Make a test results artifact.
    :return: The artifact
    """
    return TestResultsModel(
        test_suite_id=f"{TestSuite.get_default_id()}",
        test_suite=typing.cast(
            TestSuiteModel,
            ArtifactModelFactory.make(ArtifactType.TEST_SUITE).body,
        ),
        results={
            "Test1": ResultModel(
                type="Success",
                message="The RF accuracy is greater than 3",
                evidence_metadata=EvidenceMetadata(
                    test_case_id="Test1",
                    measurement=MeasurementMetadata(
                        measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
                        output_class="mlte.evidence.types.real.Real",
                        additional_data={"function": "skleran.accu()"},
                    ),
                ),
            )
        },
    )


def _make_report() -> ReportModel:
    """
    Make a report.
    :return: The artifact
    """
    return ReportModel(
        negotiation_card_id="default",
        negotiation_card=typing.cast(
            NegotiationCardModel,
            ArtifactModelFactory.make(ArtifactType.NEGOTIATION_CARD).body,
        ),
        test_suite_id="default",
        test_suite=typing.cast(
            TestSuiteModel,
            ArtifactModelFactory.make(ArtifactType.TEST_SUITE).body,
        ),
        test_results_id="default",
        test_results=typing.cast(
            TestResultsModel,
            ArtifactModelFactory.make(ArtifactType.TEST_RESULTS).body,
        ),
        comments=[CommentDescriptor(content="content")],
    )
