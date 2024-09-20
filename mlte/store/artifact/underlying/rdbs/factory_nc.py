"""
mlte/store/artifact/underlying/rdbs/factory_nc.py

Conversions between schema and internal models.
"""
from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from mlte.model.shared import (
    DataClassification,
    DataDescriptor,
    FieldDescriptor,
    GoalDescriptor,
    LabelDescriptor,
    MetricDescriptor,
    ModelDescriptor,
    ModelIODescriptor,
    ModelResourcesDescriptor,
    NegotiationCardDataModel,
    ProblemType,
    QASDescriptor,
    RiskDescriptor,
    SystemDescriptor,
)
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    DBQAS,
    DBCommentDescriptor,
    DBDataDescriptor,
    DBFieldDescriptor,
    DBGoalDescriptor,
    DBLabelDescriptor,
    DBMetricDescriptor,
    DBModelIODescriptor,
    DBModelResourcesDescriptor,
    DBNegotiationCard,
    DBNegotiationCardData,
    DBReport,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader

# -------------------------------------------------------------------------
# Negotiation Card Methods
# -------------------------------------------------------------------------


def create_negotiation_data_db_from_model(
    negotiation_card_data: NegotiationCardDataModel,
    session: Session,
) -> DBNegotiationCardData:
    """Creates the DB object from the corresponding internal model."""
    # Create intermedidate objects.
    problem_type_obj = (
        DBReader.get_problem_type(
            negotiation_card_data.system.problem_type, session
        )
        if negotiation_card_data.system.problem_type is not None
        else None
    )
    if negotiation_card_data.model.development_compute_resources:
        model_dev_resources_obj = DBModelResourcesDescriptor(
            cpu=negotiation_card_data.model.development_compute_resources.cpu,
            gpu=negotiation_card_data.model.development_compute_resources.gpu,
            memory=negotiation_card_data.model.development_compute_resources.memory,
            storage=negotiation_card_data.model.development_compute_resources.storage,
        )
    else:
        model_dev_resources_obj = None

    model_prod_resources_obj = DBModelResourcesDescriptor(
        cpu=negotiation_card_data.model.production_compute_resources.cpu,
        gpu=negotiation_card_data.model.production_compute_resources.gpu,
        memory=negotiation_card_data.model.production_compute_resources.memory,
        storage=negotiation_card_data.model.production_compute_resources.storage,
    )

    # Create the actual object.
    negotiation_card_data_obj = DBNegotiationCardData(
        sys_goals=[],
        sys_problem_type=problem_type_obj,
        sys_task=negotiation_card_data.system.task,
        sys_usage_context=negotiation_card_data.system.usage_context,
        sys_risks_fp=negotiation_card_data.system.risks.fp,
        sys_risks_fn=negotiation_card_data.system.risks.fn,
        sys_risks_other=negotiation_card_data.system.risks.other,
        model_dev_resources=model_dev_resources_obj,
        model_prod_resources=model_prod_resources_obj,
        model_prod_deployment_platform=negotiation_card_data.model.deployment_platform,
        model_prod_capability_deployment_mechanism=negotiation_card_data.model.capability_deployment_mechanism,
        model_prod_inputs=[],
        model_prod_outputs=[],
        data_descriptors=[],
        system_requirements=[],
    )

    # Create list of system goal objects.
    for goal in negotiation_card_data.system.goals:
        goal_obj = _build_goal_obj(goal)
        negotiation_card_data_obj.sys_goals.append(goal_obj)

    # Create list of data descriptor objects.
    for data_descriptor in negotiation_card_data.data:
        data_obj = _build_data_descriptor_obj(data_descriptor, session)
        negotiation_card_data_obj.data_descriptors.append(data_obj)

    # Create list of model input objects.
    for input in negotiation_card_data.model.input_specification:
        input_obj = _build_io_descriptor_obj(input)
        negotiation_card_data_obj.model_prod_inputs.append(input_obj)

    # Create list of model output objects.
    for output in negotiation_card_data.model.output_specification:
        output_obj = _build_io_descriptor_obj(output)
        negotiation_card_data_obj.model_prod_outputs.append(output_obj)

    # Create list of QAS objects.
    for qas in negotiation_card_data.system_requirements:
        qas_obj = DBQAS(
            quality=qas.quality,
            stimulus=qas.stimulus,
            source=qas.source,
            environment=qas.environment,
            response=qas.response,
            measure=qas.measure,
        )
        negotiation_card_data_obj.system_requirements.append(qas_obj)

    return negotiation_card_data_obj


def create_negotiation_db_from_model(
    negotiation_card: NegotiationCardModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBNegotiationCard:
    """Creates the DB object from the corresponding internal model."""
    # Create intermedidate objects.
    negotiation_card_data_obj = create_negotiation_data_db_from_model(
        negotiation_card.nc_data, session
    )

    # Create the actual object.
    negotiation_card_obj = DBNegotiationCard(
        artifact_header=artifact_header,
        negotiation_card_data=negotiation_card_data_obj,
    )

    return negotiation_card_obj


def create_negotiation_data_model_from_db(
    negotiation_card_data_obj: DBNegotiationCardData,
) -> NegotiationCardDataModel:
    """Creates the internal model object from the corresponding DB object."""
    body = NegotiationCardDataModel(
        system=SystemDescriptor(
            task=negotiation_card_data_obj.sys_task,
            usage_context=negotiation_card_data_obj.sys_usage_context,
            risks=RiskDescriptor(
                fp=negotiation_card_data_obj.sys_risks_fp,
                fn=negotiation_card_data_obj.sys_risks_fn,
                other=negotiation_card_data_obj.sys_risks_other,
            ),
            problem_type=ProblemType(
                negotiation_card_data_obj.sys_problem_type.name
            )
            if negotiation_card_data_obj.sys_problem_type is not None
            else None,
            goals=_build_goal_descriptors(negotiation_card_data_obj.sys_goals),
        ),
        data=_build_data_descriptors(
            negotiation_card_data_obj.data_descriptors
        ),
        model=_build_model_descriptor(
            negotiation_card_data_obj.model_dev_resources,
            negotiation_card_data_obj.model_prod_deployment_platform,
            negotiation_card_data_obj.model_prod_capability_deployment_mechanism,
            negotiation_card_data_obj.model_prod_inputs,
            negotiation_card_data_obj.model_prod_outputs,
            negotiation_card_data_obj.model_prod_resources,
        ),
        system_requirements=[
            QASDescriptor(
                quality=qas.quality,
                stimulus=qas.stimulus,
                source=qas.source,
                environment=qas.environment,
                response=qas.response,
                measure=qas.measure,
            )
            for qas in negotiation_card_data_obj.system_requirements
        ],
    )
    return body


def create_negotiation_model_from_db(
    negotiation_card_obj: DBNegotiationCard,
) -> NegotiationCardModel:
    """Creates the internal model object from the corresponding DB object."""
    return NegotiationCardModel(
        nc_data=create_negotiation_data_model_from_db(
            negotiation_card_obj.negotiation_card_data
        )
    )


# -------------------------------------------------------------------------
# Report Factory Methods
# -------------------------------------------------------------------------


def create_report_db_from_model(
    report: ReportModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBReport:
    """Creates the DB object from the corresponding internal model."""
    negotiation_card_data_obj = create_negotiation_data_db_from_model(
        report.nc_data, session
    )

    # Create the actual object.
    report_obj = DBReport(
        artifact_header=artifact_header,
        negotiation_card_data=negotiation_card_data_obj,
        validated_spec=DBReader.get_validated_spec(
            report.validated_spec_id,
            artifact_header.version_id,
            session,
        )
        if report.validated_spec_id is not None
        else None,
        comments=[],
        quantitative_analysis_content=report.quantitative_analysis.content,
    )

    # Create list of comment objects.
    for comment in report.comments:
        comment_obj = DBCommentDescriptor(content=comment.content)
        report_obj.comments.append(comment_obj)

    return report_obj


def create_report_model_from_db(report_obj: DBReport) -> ReportModel:
    """Creates the internal model object from the corresponding DB object."""
    negotiation_card_data = create_negotiation_data_model_from_db(
        report_obj.negotiation_card_data
    )

    body = ReportModel(
        nc_data=negotiation_card_data,
        validated_spec_id=report_obj.validated_spec.artifact_header.identifier
        if report_obj.validated_spec is not None
        else None,
        comments=[
            CommentDescriptor(content=comment.content)
            for comment in report_obj.comments
            if comment.content is not None
        ],
        quantitative_analysis=QuantitiveAnalysisDescriptor(
            content=report_obj.quantitative_analysis_content
        ),
    )
    return body


# -------------------------------------------------------------------------
# Common DB builder methods.
# -------------------------------------------------------------------------


def _build_goal_obj(goal: GoalDescriptor) -> DBGoalDescriptor:
    """Creates a DBGoalDescriptor object from a GoalDescriptor."""
    goal_obj = DBGoalDescriptor(description=goal.description, metrics=[])
    for metric in goal.metrics:
        metric_obj = DBMetricDescriptor(
            description=metric.description, baseline=metric.baseline
        )
        goal_obj.metrics.append(metric_obj)
    return goal_obj


def _build_data_descriptor_obj(
    data_descriptor: DataDescriptor, session: Session
) -> DBDataDescriptor:
    """Creates a DBDataDescriptor object from a DataDescriptor."""
    class_obj = (
        DBReader.get_classification_type(
            data_descriptor.classification, session
        )
        if data_descriptor.classification is not None
        else None
    )
    data_obj = DBDataDescriptor(
        description=data_descriptor.description,
        source=data_descriptor.source,
        access=data_descriptor.access,
        labeling_method=data_descriptor.labeling_method,
        rights=data_descriptor.rights,
        policies=data_descriptor.policies,
        classification=class_obj,
        labels=[],
        fields=[],
    )
    for label in data_descriptor.labels:
        label_obj = DBLabelDescriptor(
            name=label.name,
            description=label.description,
            percentage=label.percentage,
        )
        data_obj.labels.append(label_obj)
    for field in data_descriptor.fields:
        field_obj = DBFieldDescriptor(
            name=field.name,
            description=field.description,
            type=field.type,
            expected_values=field.expected_values,
            missing_values=field.missing_values,
            special_values=field.special_values,
        )
        data_obj.fields.append(field_obj)
    return data_obj


def _build_io_descriptor_obj(
    io_descriptor: ModelIODescriptor,
) -> DBModelIODescriptor:
    """Creates a DBModelIODescriptor object from a ModelIODescriptor."""
    io_descriptor_obj = DBModelIODescriptor(
        name=io_descriptor.name,
        description=io_descriptor.description,
        type=io_descriptor.type,
        expected_values=io_descriptor.expected_values,
    )
    return io_descriptor_obj


# -------------------------------------------------------------------------
# Common Artifact Model builder methods.
# -------------------------------------------------------------------------


def _build_goal_descriptors(
    goals: List[DBGoalDescriptor],
) -> List[GoalDescriptor]:
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
    data_descriptors: List[DBDataDescriptor],
) -> List[DataDescriptor]:
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
    inputs: List[DBModelIODescriptor],
    outputs: List[DBModelIODescriptor],
    prod_resources: DBModelResourcesDescriptor,
) -> ModelDescriptor:
    return ModelDescriptor(
        development_compute_resources=_build_resources(dev_resources),
        deployment_platform=deployment_platform,
        capability_deployment_mechanism=capability_deployment_mechanism,
        input_specification=[
            ModelIODescriptor(
                name=input_obj.name,
                description=input_obj.description,
                type=input_obj.type,
                expected_values=input_obj.expected_values,
            )
            for input_obj in inputs
        ],
        output_specification=[
            ModelIODescriptor(
                name=output_obj.name,
                description=output_obj.description,
                type=output_obj.type,
                expected_values=output_obj.expected_values,
            )
            for output_obj in outputs
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
