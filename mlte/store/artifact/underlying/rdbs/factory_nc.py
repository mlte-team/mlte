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
    ModelDevelopmentDescriptor,
    ModelInputDescriptor,
    ModelInterfaceDescriptor,
    ModelOutputDescriptor,
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
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    DBCommentDescriptor,
    DBDataDescriptor,
    DBFieldDescriptor,
    DBGoalDescriptor,
    DBLabelDescriptor,
    DBMetricDescriptor,
    DBModelResourcesDescriptor,
    DBNegotiationCard,
    DBReport,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader

# -------------------------------------------------------------------------
# Negotiation Card Methods
# -------------------------------------------------------------------------


def create_negotiation_db_from_model(
    negotiation_card: NegotiationCardModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBNegotiationCard:
    """Creates the DB object from the corresponding internal model."""
    # Create intermedidate objects.
    problem_type_obj = (
        DBReader.get_problem_type(negotiation_card.system.problem_type, session)
        if negotiation_card.system.problem_type is not None
        else None
    )
    model_dev_resources_obj = DBModelResourcesDescriptor(
        cpu=negotiation_card.model.development.resources.cpu,
        gpu=negotiation_card.model.development.resources.gpu,
        memory=negotiation_card.model.development.resources.memory,
        storage=negotiation_card.model.development.resources.storage,
    )
    model_prod_resources_obj = DBModelResourcesDescriptor(
        cpu=negotiation_card.model.production.resources.cpu,
        gpu=negotiation_card.model.production.resources.gpu,
        memory=negotiation_card.model.production.resources.memory,
        storage=negotiation_card.model.production.resources.storage,
    )

    # Create the actual object.
    negotiation_card_obj = DBNegotiationCard(
        artifact_header=artifact_header,
        sys_goals=[],
        sys_problem_type=problem_type_obj,
        sys_task=negotiation_card.system.task,
        sys_usage_context=negotiation_card.system.usage_context,
        sys_risks_fp=negotiation_card.system.risks.fp,
        sys_risks_fn=negotiation_card.system.risks.fn,
        sys_risks_other=negotiation_card.system.risks.other,
        model_dev_resources=model_dev_resources_obj,
        model_prod_resources=model_prod_resources_obj,
        model_prod_deployment_platform=negotiation_card.model.production.deployment_platform,
        model_prod_capability_deployment_mechanism=negotiation_card.model.production.capability_deployment_mechanism,
        model_prod_interface_input_desc=negotiation_card.model.production.interface.input.description,
        model_prod_interface_output_desc=negotiation_card.model.production.interface.output.description,
        data_descriptors=[],
    )

    # Create list of system goal objects.
    for goal in negotiation_card.system.goals:
        goal_obj = _build_goal_obj(goal)
        negotiation_card_obj.sys_goals.append(goal_obj)

    # Create list of data descriptor objects.
    for data_descriptor in negotiation_card.data:
        data_obj = _build_data_descriptor_obj(data_descriptor, session)
        negotiation_card_obj.data_descriptors.append(data_obj)

    return negotiation_card_obj


def create_negotiation_model_from_db(
    negotiation_obj: DBNegotiationCard,
) -> NegotiationCardModel:
    """Creates the internal model object from the corresponding DB object."""
    body = NegotiationCardModel(
        system=SystemDescriptor(
            task=negotiation_obj.sys_task,
            usage_context=negotiation_obj.sys_usage_context,
            risks=RiskDescriptor(
                fp=negotiation_obj.sys_risks_fp,
                fn=negotiation_obj.sys_risks_fn,
                other=negotiation_obj.sys_risks_other,
            ),
            problem_type=ProblemType(negotiation_obj.sys_problem_type.name)
            if negotiation_obj.sys_problem_type is not None
            else None,
            goals=_build_goal_descriptors(negotiation_obj.sys_goals),
        ),
        data=_build_data_descriptors(negotiation_obj.data_descriptors),
        model=ModelDescriptor(
            development=ModelDevelopmentDescriptor(
                resources=_build_resources(negotiation_obj.model_dev_resources)
            ),
            production=_build_model_prod_descriptor(
                negotiation_obj.model_prod_deployment_platform,
                negotiation_obj.model_prod_capability_deployment_mechanism,
                negotiation_obj.model_prod_interface_input_desc,
                negotiation_obj.model_prod_interface_output_desc,
                negotiation_obj.model_prod_resources,
            ),
        ),
    )
    return body


# -------------------------------------------------------------------------
# Report Factory Methods
# -------------------------------------------------------------------------


def create_report_db_from_model(
    report: ReportModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBReport:
    """Creates the DB object from the corresponding internal model."""
    # Create intermedidate objects.
    problem_type_obj = (
        DBReader.get_problem_type(report.summary.problem_type, session)
        if report.summary.problem_type is not None
        else None
    )
    model_prod_resources_obj = DBModelResourcesDescriptor(
        cpu=report.intended_use.production_requirements.resources.cpu,
        gpu=report.intended_use.production_requirements.resources.gpu,
        memory=report.intended_use.production_requirements.resources.memory,
        storage=report.intended_use.production_requirements.resources.storage,
    )

    # Create the actual object.
    report_obj = DBReport(
        artifact_header=artifact_header,
        summary_problem_type=problem_type_obj,
        summary_task=report.summary.task,
        validated_spec=DBReader.get_validated_spec(
            report.performance.validated_spec_id,
            artifact_header.version_id,
            session,
        )
        if report.performance.validated_spec_id is not None
        else None,
        performance_goals=[],
        intended_usage_context=report.intended_use.usage_context,
        intended_reqs_model_prod_deployment_platform=report.intended_use.production_requirements.deployment_platform,
        intended_reqs_model_prod_capability_deployment_mechanism=report.intended_use.production_requirements.capability_deployment_mechanism,
        intended_reqs_model_prod_interface_input_desc=report.intended_use.production_requirements.interface.input.description,
        intended_reqs_model_prod_interface_output_desc=report.intended_use.production_requirements.interface.output.description,
        intended_reqs_model_prod_resources=model_prod_resources_obj,
        risks_fp=report.risks.fp,
        risks_fn=report.risks.fn,
        risks_other=report.risks.other,
        data_descriptors=[],
        comments=[],
        quantitative_analysis_content=report.quantitative_analysis.content,
    )

    # Create list of goal objects.
    for goal in report.performance.goals:
        goal_obj = _build_goal_obj(goal)
        report_obj.performance_goals.append(goal_obj)

    # Create list of data descriptor objects.
    for data_descriptor in report.data:
        data_obj = _build_data_descriptor_obj(data_descriptor, session)
        report_obj.data_descriptors.append(data_obj)

    # Create list of comment objects.
    for comment in report.comments:
        comment_obj = DBCommentDescriptor(content=comment.content)
        report_obj.comments.append(comment_obj)

    return report_obj


def create_report_model_from_db(report_obj: DBReport) -> ReportModel:
    """Creates the internal model object from the corresponding DB object."""
    body = ReportModel(
        summary=SummaryDescriptor(
            problem_type=ProblemType(report_obj.summary_problem_type.name)
            if report_obj.summary_problem_type is not None
            else None,
            task=report_obj.summary_task,
        ),
        performance=PerformanceDesciptor(
            goals=_build_goal_descriptors(report_obj.performance_goals),
            validated_spec_id=report_obj.validated_spec.artifact_header.identifier
            if report_obj.validated_spec is not None
            else None,
        ),
        intended_use=IntendedUseDescriptor(
            usage_context=report_obj.intended_usage_context,
            production_requirements=_build_model_prod_descriptor(
                report_obj.intended_reqs_model_prod_deployment_platform,
                report_obj.intended_reqs_model_prod_capability_deployment_mechanism,
                report_obj.intended_reqs_model_prod_interface_input_desc,
                report_obj.intended_reqs_model_prod_interface_output_desc,
                report_obj.intended_reqs_model_prod_resources,
            ),
        ),
        risks=RiskDescriptor(
            fp=report_obj.risks_fp,
            fn=report_obj.risks_fn,
            other=report_obj.risks_other,
        ),
        data=_build_data_descriptors(report_obj.data_descriptors),
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


def _build_model_prod_descriptor(
    deployment_platform: Optional[str],
    capability_deployment_mechanism: Optional[str],
    input: Optional[str],
    output: Optional[str],
    resources: Optional[DBModelResourcesDescriptor],
) -> ModelProductionDescriptor:
    return ModelProductionDescriptor(
        deployment_platform=deployment_platform,
        capability_deployment_mechanism=capability_deployment_mechanism,
        interface=ModelInterfaceDescriptor(
            input=ModelInputDescriptor(description=input),
            output=ModelOutputDescriptor(description=output),
        ),
        resources=_build_resources(resources),
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
