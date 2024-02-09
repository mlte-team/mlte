"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing
from typing import List, Optional

from sqlalchemy.orm import Session

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
    IntendedUseDescriptor,
    PerformanceDesciptor,
    ReportModel,
    SummaryDescriptor,
)
from mlte.spec.model import ConditionModel, PropertyModel, SpecModel
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
)
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
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBCondition,
    DBProperty,
    DBResult,
    DBSpec,
    DBValidatedSpec,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.validation.model import ResultModel, ValidatedSpecModel

# -------------------------------------------------------------------------
# DB artifact factory.
# -------------------------------------------------------------------------


def create_db_artifact(
    artifact: ArtifactModel,
    artifact_type_obj: DBArtifactType,
    version_id: int,
    session: Session,
) -> typing.Union[DBSpec, DBValidatedSpec, DBNegotiationCard, DBReport]:
    """Converts an internal model to its corresponding DB object for artifacts."""
    artifact_header = DBArtifactHeader(
        identifier=artifact.header.identifier,
        type=artifact_type_obj,
        timestamp=artifact.header.timestamp,
        version_id=version_id,
    )

    if artifact.header.type == ArtifactType.SPEC:
        # Create a DBSpec and its internal lists: properties, and inside them, conditions.
        spec = typing.cast(SpecModel, artifact.body)
        spec_obj = DBSpec(artifact_header=artifact_header, properties=[])
        for property in spec.properties:
            property_obj = DBProperty(
                name=property.name,
                description=property.description,
                rationale=property.rationale,
                module=property.module,
                spec=spec_obj,
            )
            spec_obj.properties.append(property_obj)

            for measurement_id, condition in property.conditions.items():
                condition_obj = DBCondition(
                    name=condition.name,
                    measurement_id=measurement_id,
                    arguments=" ".join(str(x) for x in condition.arguments),
                    callback=condition.callback,
                    value_class=condition.value_class,
                    property=property_obj,
                )
                property_obj.conditions.append(condition_obj)

        return spec_obj
    elif artifact.header.type == ArtifactType.VALIDATED_SPEC:
        # Create a DBValidatedSpec db object.
        validated_spec = typing.cast(ValidatedSpecModel, artifact.body)
        validated_spec_obj = DBValidatedSpec(
            artifact_header=artifact_header,
            results=[],
            spec=validated_spec.spec,
        )
        for property_name, results in validated_spec.results.items():
            for measurement_id, result in results.items():
                result_obj = DBResult(
                    measurement_id=measurement_id,
                    type=result.type,
                    message=result.message,
                    property=DBReader.get_property(
                        validated_spec.spec_identifier, property_name, session
                    ),
                    validated_spec=validated_spec_obj,
                )
                validated_spec_obj.results.append(result_obj)
        return validated_spec_obj
    elif artifact.header.type == ArtifactType.NEGOTIATION_CARD:
        # Create a DBNegotiationCard object and all its subpieces.
        negotiation_card = typing.cast(NegotiationCardModel, artifact.body)

        # Create intermedidate objects.
        problem_type_obj = (
            DBReader.get_problem_type(
                negotiation_card.system.problem_type, session
            )
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
            model_prod_integration=negotiation_card.model.production.integration,
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
    elif artifact.header.type == ArtifactType.REPORT:
        # Create a DBReport object and all its subpieces.
        report = typing.cast(ReportModel, artifact.body)

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
            performance_findings=report.performance.findings,
            performance_goals=[],
            intended_usage_context=report.intended_use.usage_context,
            intended_reqs_model_prod_integration=report.intended_use.production_requirements.integration,
            intended_reqs_model_prod_interface_input_desc=report.intended_use.production_requirements.interface.input.description,
            intended_reqs_model_prod_interface_output_desc=report.intended_use.production_requirements.interface.output.description,
            intended_reqs_model_prod_resources=model_prod_resources_obj,
            risks_fp=report.risks.fp,
            risks_fn=report.risks.fn,
            risks_other=report.risks.other,
            data_descriptors=[],
            comments=[],
            quantitative_analysis_content=report.quantitative_analysis.content,
            #    validated_spec: Mapped[DBValidatedSpec] = relationship()
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
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )


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
        rights=data_descriptor.rights,
        policies=data_descriptor.policies,
        identifiable_information=data_descriptor.identifiable_information,
        classification=class_obj,
        labels=[],
        fields=[],
    )
    for label in data_descriptor.labels:
        label_obj = DBLabelDescriptor(
            description=label.description, percentage=label.percentage
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
# Artifact model factory.
# -------------------------------------------------------------------------


def create_artifact_from_db(
    artifact_header_obj: DBArtifactHeader,
) -> ArtifactModel:
    """
    Creates an Artifact model from the corresponding DB object and DB header.

    :param artifact_header_obj: A DBArtifactHeader object from the DB with header info.
    :param artifact_obj: A DB object of the specific artifact type with the artifact info.
    :return: the DB data converted into an ArtifactModel.
    """
    artifact_header = ArtifactHeaderModel(
        identifier=artifact_header_obj.identifier,
        type=ArtifactType(artifact_header_obj.type.name),
        timestamp=artifact_header_obj.timestamp,
    )

    body: typing.Union[
        SpecModel, ValidatedSpecModel, NegotiationCardModel, ReportModel
    ]
    if artifact_header.type == ArtifactType.SPEC:
        # Creating a Spec from DB data.
        spec_obj = typing.cast(DBSpec, artifact_header_obj.body_spec)
        body = SpecModel(
            artifact_type=artifact_header.type,
            properties=[
                PropertyModel(
                    name=property.name,
                    description=property.description,
                    rationale=property.rationale,
                    module=property.module,
                    conditions={
                        condition.measurement_id: ConditionModel(
                            name=condition.name,
                            callback=condition.callback,
                            value_class=condition.value_class,
                            arguments=condition.arguments.split(" "),
                        )
                        for condition in property.conditions
                    },
                )
                for property in spec_obj.properties
            ],
        )
    elif artifact_header.type == ArtifactType.VALIDATED_SPEC:
        # Creating a ValidatedSpec from DB data.
        validated_obj = typing.cast(
            DBValidatedSpec, artifact_header_obj.body_validated_spec
        )
        body = ValidatedSpecModel(
            artifact_type=artifact_header.type,
            results={
                property.name: {
                    result.measurement_id: ResultModel(
                        type=result.type,
                        message=result.message,
                        metadata=EvidenceMetadata(
                            measurement_type=result.evidence_metadata.measurement_type,
                            identifier=Identifier(
                                name=result.evidence_metadata.identifier
                            ),
                        ),
                    )
                    for result in validated_obj.results
                    if result.property.name == property.name
                }
                for property in validated_obj.spec.properties
            }
            if validated_obj.spec is not None
            else {},
        )
    elif artifact_header.type == ArtifactType.NEGOTIATION_CARD:
        # Creating a NegotiationCard from DB data.
        negotiation_obj = typing.cast(
            DBNegotiationCard, artifact_header_obj.body_negotiation_card
        )
        body = NegotiationCardModel(
            artifact_type=artifact_header.type,
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
                    resources=_build_resources(
                        negotiation_obj.model_dev_resources
                    )
                ),
                production=_build_model_prod_descriptor(
                    negotiation_obj.model_prod_integration,
                    negotiation_obj.model_prod_interface_input_desc,
                    negotiation_obj.model_prod_interface_output_desc,
                    negotiation_obj.model_prod_resources,
                ),
            ),
        )
    elif artifact_header.type == ArtifactType.REPORT:
        # Creating a Report from DB data.
        report_obj = typing.cast(DBReport, artifact_header_obj.body_report)
        body = ReportModel(
            artifact_type=artifact_header.type,
            summary=SummaryDescriptor(
                problem_type=ProblemType(report_obj.summary_problem_type.name)
                if report_obj.summary_problem_type is not None
                else None,
                task=report_obj.summary_task,
            ),
            performance=PerformanceDesciptor(
                goals=_build_goal_descriptors(report_obj.performance_goals),
                findings=report_obj.performance_findings,
            ),
            intended_use=IntendedUseDescriptor(
                usage_context=report_obj.intended_usage_context,
                production_requirements=_build_model_prod_descriptor(
                    report_obj.intended_reqs_model_prod_integration,
                    report_obj.intended_reqs_model_prod_interface_input_desc,
                    report_obj.intended_reqs_model_prod_interface_output_desc,
                    report_obj.intended_reqs_model_prod_resources,
                ),
            ),
            risks=RiskDescriptor(
                fp=report_obj.risks_fn,
                fn=report_obj.risks_fn,
                other=report_obj.risks_other,
            ),
            data=_build_data_descriptors(report_obj.data_descriptors),
        )
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)


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
            rights=data_descriptor.rights,
            policies=data_descriptor.policies,
            identifiable_information=data_descriptor.identifiable_information,
            labels=[
                LabelDescriptor(
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
    integration: Optional[str],
    input: Optional[str],
    output: Optional[str],
    resources: Optional[DBModelResourcesDescriptor],
) -> ModelProductionDescriptor:
    return ModelProductionDescriptor(
        integration=integration,
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
