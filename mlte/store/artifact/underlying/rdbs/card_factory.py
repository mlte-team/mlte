"""Conversions between schema and internal DB models."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

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
    SystemDescriptor,
)
from mlte.negotiation.qas import QASDescriptor
from mlte.store.artifact.underlying.rdbs.card_metadata import (
    DBQAS,
    DBDataDescriptor,
    DBFieldDescriptor,
    DBGeneralRisk,
    DBGoalDescriptor,
    DBLabelDescriptor,
    DBMetricDescriptor,
    DBModelIODescriptor,
    DBModelResourcesDescriptor,
    DBNegotiationCard,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact
from mlte.store.artifact.underlying.rdbs.reader import DBReader

# -------------------------------------------------------------------------
# Negotiation Card Methods
# -------------------------------------------------------------------------


def create_card_orm(
    negotiation_card: NegotiationCardModel,
    artifact_orm: Optional[DBArtifact],
    session: Session,
) -> DBNegotiationCard:
    """Creates the DB object from the corresponding internal model."""
    # Create intermedidate objects.
    problem_type_orm = (
        DBReader.get_problem_type(negotiation_card.system.problem_type, session)
        if negotiation_card.system.problem_type is not None
        else None
    )
    if negotiation_card.model.development_compute_resources:
        model_dev_resources_orm = DBModelResourcesDescriptor(
            cpu=negotiation_card.model.development_compute_resources.cpu,
            gpu=negotiation_card.model.development_compute_resources.gpu,
            memory=negotiation_card.model.development_compute_resources.memory,
            storage=negotiation_card.model.development_compute_resources.storage,
        )
    else:
        model_dev_resources_orm = None

    model_prod_resources_orm = DBModelResourcesDescriptor(
        cpu=negotiation_card.model.production_compute_resources.cpu,
        gpu=negotiation_card.model.production_compute_resources.gpu,
        memory=negotiation_card.model.production_compute_resources.memory,
        storage=negotiation_card.model.production_compute_resources.storage,
    )

    # Create the actual object.
    negotiation_card_orm = DBNegotiationCard(
        artifact=artifact_orm,
        sys_goals=[],
        sys_problem_type=problem_type_orm,
        sys_task=negotiation_card.system.task,
        sys_usage_context=negotiation_card.system.usage_context,
        sys_risks=[],
        model_dev_resources=model_dev_resources_orm,
        model_prod_resources=model_prod_resources_orm,
        model_prod_deployment_platform=negotiation_card.model.deployment_platform,
        model_prod_capability_deployment_mechanism=negotiation_card.model.capability_deployment_mechanism,
        model_prod_model_source=negotiation_card.model.model_source,
        model_prod_inputs=[],
        model_prod_outputs=[],
        data_descriptors=[],
        system_requirements=[],
    )

    # Create list of risks.
    for risk in negotiation_card.system.risks:
        risk_orm = DBGeneralRisk(description=risk)
        negotiation_card_orm.sys_risks.append(risk_orm)

    # Create list of system goal objects.
    for goal in negotiation_card.system.goals:
        goal_orm = _build_goal_orm(goal)
        negotiation_card_orm.sys_goals.append(goal_orm)

    # Create list of data descriptor objects.
    for data_descriptor in negotiation_card.data:
        data_orm = _build_data_descriptor_orm(data_descriptor, session)
        negotiation_card_orm.data_descriptors.append(data_orm)

    # Create list of model input objects.
    for input in negotiation_card.model.input_specification:
        input_orm = _build_io_descriptor_orm(input)
        negotiation_card_orm.model_prod_inputs.append(input_orm)

    # Create list of model output objects.
    for output in negotiation_card.model.output_specification:
        output_orm = _build_io_descriptor_orm(output)
        negotiation_card_orm.model_prod_outputs.append(output_orm)

    # Create list of QAS objects.
    for qas in negotiation_card.system_requirements:
        qas_orm = DBQAS(
            identifier=qas.identifier,
            quality=qas.quality,
            stimulus=qas.stimulus,
            source=qas.source,
            environment=qas.environment,
            response=qas.response,
            measure=qas.measure,
        )
        negotiation_card_orm.system_requirements.append(qas_orm)

    return negotiation_card_orm


def create_card_model(
    negotiation_card_orm: DBNegotiationCard,
) -> NegotiationCardModel:
    """Creates the internal model object from the corresponding DB object."""
    body = NegotiationCardModel(
        system=SystemDescriptor(
            task=negotiation_card_orm.sys_task,
            usage_context=negotiation_card_orm.sys_usage_context,
            risks=[risk.description for risk in negotiation_card_orm.sys_risks],
            problem_type=(
                ProblemType(negotiation_card_orm.sys_problem_type.name)
                if negotiation_card_orm.sys_problem_type is not None
                else None
            ),
            goals=_build_goal_descriptors(negotiation_card_orm.sys_goals),
        ),
        data=_build_data_descriptors(negotiation_card_orm.data_descriptors),
        model=_build_model_descriptor(
            negotiation_card_orm.model_dev_resources,
            negotiation_card_orm.model_prod_deployment_platform,
            negotiation_card_orm.model_prod_capability_deployment_mechanism,
            negotiation_card_orm.model_prod_model_source,
            negotiation_card_orm.model_prod_inputs,
            negotiation_card_orm.model_prod_outputs,
            negotiation_card_orm.model_prod_resources,
        ),
        system_requirements=[
            QASDescriptor(
                identifier=qas.identifier,
                quality=qas.quality,
                stimulus=qas.stimulus,
                source=qas.source,
                environment=qas.environment,
                response=qas.response,
                measure=qas.measure,
            )
            for qas in negotiation_card_orm.system_requirements
        ],
    )
    return body


# -------------------------------------------------------------------------
# Common DB builder methods.
# -------------------------------------------------------------------------


def _build_goal_orm(goal: GoalDescriptor) -> DBGoalDescriptor:
    """Creates a DBGoalDescriptor object from a GoalDescriptor."""
    goal_orm = DBGoalDescriptor(description=goal.description, metrics=[])
    for metric in goal.metrics:
        metric_orm = DBMetricDescriptor(
            description=metric.description, baseline=metric.baseline
        )
        goal_orm.metrics.append(metric_orm)
    return goal_orm


def _build_data_descriptor_orm(
    data_descriptor: DataDescriptor, session: Session
) -> DBDataDescriptor:
    """Creates a DBDataDescriptor object from a DataDescriptor."""
    class_orm = (
        DBReader.get_classification_type(
            data_descriptor.classification, session
        )
        if data_descriptor.classification is not None
        else None
    )
    data_orm = DBDataDescriptor(
        description=data_descriptor.description,
        source=data_descriptor.source,
        access=data_descriptor.access,
        labeling_method=data_descriptor.labeling_method,
        rights=data_descriptor.rights,
        policies=data_descriptor.policies,
        classification=class_orm,
        labels=[],
        fields=[],
    )
    for label in data_descriptor.labels:
        label_orm = DBLabelDescriptor(
            name=label.name,
            description=label.description,
            percentage=label.percentage,
        )
        data_orm.labels.append(label_orm)
    for field in data_descriptor.fields:
        field_orm = DBFieldDescriptor(
            name=field.name,
            description=field.description,
            type=field.type,
            expected_values=field.expected_values,
            missing_values=field.missing_values,
            special_values=field.special_values,
        )
        data_orm.fields.append(field_orm)
    return data_orm


def _build_io_descriptor_orm(
    io_descriptor: ModelIODescriptor,
) -> DBModelIODescriptor:
    """Creates a DBModelIODescriptor object from a ModelIODescriptor."""
    io_descriptor_orm = DBModelIODescriptor(
        name=io_descriptor.name,
        description=io_descriptor.description,
        type=io_descriptor.type,
        expected_values=io_descriptor.expected_values,
    )
    return io_descriptor_orm


# -------------------------------------------------------------------------
# Common Artifact Model builder methods.
# -------------------------------------------------------------------------


def _build_goal_descriptors(
    goals: list[DBGoalDescriptor],
) -> list[GoalDescriptor]:
    """Build a list of GoalDescriptors from DBGoalDescriptors."""
    return [
        GoalDescriptor(
            description=goal.description,
            metrics=[
                MetricDescriptor(
                    description=metric.description,
                    baseline=metric.baseline,
                )
                for metric in goal.metrics
            ],
        )
        for goal in goals
    ]


def _build_data_descriptors(
    data_descriptors: list[DBDataDescriptor],
) -> list[DataDescriptor]:
    """Build a list of DataDescriptor from DBDataDescriptor."""
    return [
        DataDescriptor(
            description=data_descriptor.description,
            source=data_descriptor.source,
            classification=DataClassification(
                data_descriptor.classification.name
            ),
            access=data_descriptor.access,
            labeling_method=data_descriptor.labeling_method,
            rights=data_descriptor.rights,
            policies=data_descriptor.policies,
            labels=[
                LabelDescriptor(
                    name=label.name,
                    description=label.description,
                    percentage=label.percentage,
                )
                for label in data_descriptor.labels
            ],
            fields=[
                FieldDescriptor(
                    name=field.name,
                    description=field.description,
                    type=field.type,
                    expected_values=field.expected_values,
                    missing_values=field.missing_values,
                    special_values=field.special_values,
                )
                for field in data_descriptor.fields
            ],
        )
        for data_descriptor in data_descriptors
    ]


def _build_model_descriptor(
    dev_resources: DBModelResourcesDescriptor,
    deployment_platform: Optional[str],
    capability_deployment_mechanism: Optional[str],
    model_source: Optional[str],
    inputs: list[DBModelIODescriptor],
    outputs: list[DBModelIODescriptor],
    prod_resources: DBModelResourcesDescriptor,
) -> ModelDescriptor:
    """Build a ModelDescriptor from a set of data fror the model."""
    return ModelDescriptor(
        development_compute_resources=_build_resources(dev_resources),
        deployment_platform=deployment_platform,
        capability_deployment_mechanism=capability_deployment_mechanism,
        model_source=model_source,
        input_specification=[
            ModelIODescriptor(
                name=input_orm.name,
                description=input_orm.description,
                type=input_orm.type,
                expected_values=input_orm.expected_values,
            )
            for input_orm in inputs
        ],
        output_specification=[
            ModelIODescriptor(
                name=output_orm.name,
                description=output_orm.description,
                type=output_orm.type,
                expected_values=output_orm.expected_values,
            )
            for output_orm in outputs
        ],
        production_compute_resources=_build_resources(prod_resources),
    )


def _build_resources(
    resources: Optional[DBModelResourcesDescriptor],
) -> ModelResourcesDescriptor:
    """Build a ModelResourcesDescriptor from DBModelResourcesDescriptor."""
    return ModelResourcesDescriptor(
        cpu=resources.cpu if resources else None,
        gpu=resources.gpu if resources else None,
        memory=resources.memory if resources else None,
        storage=resources.storage if resources else None,
    )
