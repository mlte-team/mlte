"""
test/fixture/artifact.py

Unit test support for artifact generation.
"""

from __future__ import annotations

import random
import string
from typing import Generator, List, Union

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata, Identifier
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
    ProblemType,
    RiskDescriptor,
)
from mlte.negotiation.model import NegotiationCardModel, SystemDescriptor
from mlte.report.model import (
    CommentDescriptor,
    IntendedUseDescriptor,
    PerformanceDesciptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
    SummaryDescriptor,
)
from mlte.spec.model import ConditionModel, PropertyModel, SpecModel
from mlte.validation.model import ResultModel, ValidatedSpecModel
from mlte.value.model import IntegerValueModel, ValueModel
from mlte.value.types.integer import Integer


def _random_id(length: int = 5) -> str:
    """
    Generate a random identifier.
    :param length: The length of the ID
    :return: The identifier
    """
    return "".join(random.choices(string.ascii_lowercase, k=length))


def artifact_types() -> Generator[ArtifactType, None, None]:
    """A generator over artifact types."""
    for type in ArtifactType:
        yield type


class ArtifactFactory:
    """A class for build artifacts."""

    @staticmethod
    def make(
        type: ArtifactType, id: str = _random_id(), complete: bool = False
    ) -> ArtifactModel:
        """
        Construct an artifact model of the given type.
        :param type: The artifact type
        :param id: The artifact identifier (default: randomly generated)
        :param complete: Whether to create a complete, fully defined artifact model (True), or a simple empty one (False)
        :return: The artifact model
        """
        return ArtifactModel(
            header=ArtifactHeaderModel(identifier=id, type=type),
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


def _make_body(
    type: ArtifactType, id: str, complete: bool
) -> Union[
    NegotiationCardModel, ValueModel, SpecModel, ValidatedSpecModel, ReportModel
]:
    """
    Make the body of the artifact for a given type.
    :param type: The artifact type
    :param id: The identifier for the artifact
    :return: The artifact body model
    """
    if type == ArtifactType.NEGOTIATION_CARD:
        return _make_negotiation_card(complete)
    if type == ArtifactType.VALUE:
        return _make_value(id, complete)
    if type == ArtifactType.SPEC:
        return _make_spec(complete)
    if type == ArtifactType.VALIDATED_SPEC:
        return _make_validated_spec(complete)
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


def _make_value(id: str, complete: bool) -> ValueModel:
    """
    Make a minimal value, or a fully featured one, depending on complete.
    :return: The artifact
    """
    m = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name=id)
    )

    return ValueModel(
        metadata=m,
        value_class=Integer.get_class_path(),
        value=IntegerValueModel(
            integer=1,
        ),
    )


def _make_spec(complete: bool) -> SpecModel:
    """
    Make a minimal spec, or a fully featured one, depending on complete.
    :return: The artifact
    """
    if not complete:
        return SpecModel()
    else:
        return make_complete_spec_model()


def _make_validated_spec(complete: bool) -> ValidatedSpecModel:
    """
    Make a minimal validated spec, or a fully featured one, depending on complete.
    :return: The artifact
    """
    # TODO: Make a complete VSpec that is properly connected to Spec and Properties, which is not trivial.
    # Maybe create in DB here? Find way to make this work for better coverage.
    return ValidatedSpecModel()


def _make_report(complete: bool) -> ReportModel:
    """
    Make a minimal report, or a fully featured one, depending on complete.
    :return: The artifact
    """
    if not complete:
        return ReportModel()
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
            development=ModelDevelopmentDescriptor(
                resources=ModelResourcesDescriptor(
                    cpu="cpu", gpu="gpu", memory="memory", storage="storage"
                )
            ),
            production=ModelProductionDescriptor(
                deployment_platform="local server",
                capability_deployment_mechanism="API",
                interface=ModelInterfaceDescriptor(
                    input=ModelIODescriptor(
                        name="i1", description="description", type="string"
                    ),
                    output=ModelIODescriptor(
                        name="o1", description="description", type="string"
                    ),
                ),
                resources=ModelResourcesDescriptor(
                    cpu="cpu",
                    gpu="gpu",
                    memory="memory",
                    storage="storage",
                ),
            ),
        ),
    )


def make_complete_spec_model() -> SpecModel:
    """
    Make a filled in Spec model.
    :return: The artifact model
    """
    return SpecModel(
        properties=[
            PropertyModel(
                name="TaskEfficacy",
                description="Property for useful things.",
                rationale="Because I say so",
                module="mlte.properties.functionality.task_efficacy",
                conditions={
                    "accuracy": ConditionModel(
                        name="less_than",
                        arguments=[3.0],
                        callback="invalid^#*@&^ASD@#",
                        value_class="mlte.value.types.real.Real",
                    )
                },
            )
        ],
    )


def make_complete_validated_spec_model() -> ValidatedSpecModel:
    """
    Make a filled in ValidatedSpec model.
    :return: The artifact model
    """
    return ValidatedSpecModel(
        spec_identifier="",
        spec=make_complete_spec_model(),
        results={
            "TaskEfficacy": {
                "accuracy": ResultModel(
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
    )


def make_complete_report() -> ReportModel:
    """
    Make a filled in Report model.
    :return: The artifact model
    """
    return ReportModel(
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
                deployment_platform="local server",
                capability_deployment_mechanism="API",
                interface=ModelInterfaceDescriptor(
                    input=ModelIODescriptor(
                        name="i1", description="description", type="string"
                    ),
                    output=ModelIODescriptor(
                        name="o1", description="description", type="string"
                    ),
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
        comments=[CommentDescriptor(content="content")],
        quantitative_analysis=QuantitiveAnalysisDescriptor(content="analysis"),
    )
