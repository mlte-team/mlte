"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

from __future__ import annotations

import random
import string
from typing import List, Optional, Union

from mlte._private import meta
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
from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.results.model import ResultModel, TestResultsModel
from mlte.tests.model import TestCaseModel, TestSuiteModel
from mlte.validation.validator import Validator
from test.evidence.types.helper import get_sample_evidence_metadata


def _random_id(length: int = 5) -> str:
    """
    Generate a random identifier.
    :param length: The length of the ID
    :return: The identifier
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


class ArtifactFactory:
    """A class for build artifacts."""

    @staticmethod
    def make(
        type: ArtifactType,
        id: str = _random_id(),
        user: Optional[str] = None,
        complete: bool = False,
    ) -> ArtifactModel:
        """
        Construct an artifact model of the given type.
        :param type: The artifact type
        :param id: The artifact identifier (default: randomly generated)
        :param complete: Whether to create a complete, fully defined artifact model (True), or a simple empty one (False)
        :return: The artifact model
        """
        return ArtifactModel(
            header=ArtifactHeaderModel(identifier=id, type=type, creator=user),
            body=_make_body(type, id, complete),
        )


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


def _make_body(type: ArtifactType, id: str, complete: bool) -> Union[
    NegotiationCardModel,
    EvidenceModel,
    TestSuiteModel,
    TestResultsModel,
    ReportModel,
]:
    """
    Make the body of the artifact for a given type.
    :param type: The artifact type
    :param id: The identifier for the artifact
    :return: The artifact body model
    """
    if type == ArtifactType.NEGOTIATION_CARD:
        return _make_negotiation_card(complete)
    if type == ArtifactType.EVIDENCE:
        return _make_value(id, complete)
    if type == ArtifactType.TEST_SUITE:
        return _make_test_suite(complete)
    if type == ArtifactType.TEST_RESULTS:
        return _make_test_results(complete)
    if type == ArtifactType.REPORT:
        return _make_report(complete)

    assert False, f"Unkown artifact type provided when creating body: {type}."


def _make_negotiation_card(complete: bool) -> NegotiationCardModel:
    """
    Make a minimal negotiation card, or a fully featured one, depending on complete.
    :return: The artifact
    """
    if not complete:
        return NegotiationCardModel()
    else:
        return make_complete_negotiation_card()


def _make_value(id: str, complete: bool) -> EvidenceModel:
    """
    Make a minimal value, or a fully featured one, depending on complete.
    :return: The artifact
    """
    m = get_sample_evidence_metadata(test_case_id=id)

    return EvidenceModel(
        metadata=m,
        evidence_class=meta.get_qualified_name(Integer),
        value=IntegerValueModel(integer=1),
    )


def _make_test_suite(complete: bool) -> TestSuiteModel:
    """
    Make a minimal test suite, or a fully featured one, depending on complete.
    :return: The artifact
    """
    if not complete:
        return TestSuiteModel()
    else:
        return make_complete_test_suite_model()


def _make_test_results(complete: bool) -> TestResultsModel:
    """
    Make a minimal test results, or a fully featured one, depending on complete.
    :return: The artifact
    """
    test_suite = make_complete_test_suite_model()
    return TestResultsModel(test_suite=test_suite)


def _make_report(complete: bool) -> ReportModel:
    """
    Make a minimal report, or a fully featured one, depending on complete.
    :return: The artifact
    """
    if not complete:
        raise RuntimeError("Report needs to have all basic fields filled in.")
    else:
        return make_complete_report()


def make_complete_negotiation_card() -> NegotiationCardModel:
    """
    Make a filled in NegotiationCard model.
    :return: The artifact model
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
            risks=RiskDescriptor(fp="fp", fn="fn", other="other"),
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
                identifier="default.negotiation_card-qas_1",
                quality="fairness",
                stimulus="new data arrives",
                source="from new area",
                environment="normal time",
                response="results are fair",
                measure="less than 1 percent difference",
            ),
        ],
    )


def make_complete_test_suite_model() -> TestSuiteModel:
    """
    Make a filled in TestSuite model.
    :return: The artifact model
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


def make_complete_test_results_model() -> TestResultsModel:
    """
    Make a filled in TestResults model.
    :return: The artifact model
    """
    return TestResultsModel(
        test_suite_id="",
        test_suite=make_complete_test_suite_model(),
        results={
            "accuracy": ResultModel(
                type="Success",
                message="The RF accuracy is greater than 3",
                evidence_metadata=EvidenceMetadata(
                    test_case_id="accuracy",
                    measurement=MeasurementMetadata(
                        measurement_class="mlte.measurement.external_measurement.ExternalMeasurement",
                        output_class="mlte.evidence.types.real.Real",
                        additional_data={"function": "skleran.accu()"},
                    ),
                ),
            )
        },
    )


def make_complete_report() -> ReportModel:
    """
    Make a filled in Report model.
    :return: The artifact model
    """
    return ReportModel(
        negotiation_card_id="default",
        negotiation_card=_make_negotiation_card(complete=True),
        test_suite_id="default",
        test_suite=_make_test_suite(complete=True),
        test_results_id="default",
        test_results=_make_test_results(complete=True),
        comments=[CommentDescriptor(content="content")],
        quantitative_analysis=QuantitiveAnalysisDescriptor(content="analysis"),
    )
