"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing

from sqlalchemy.orm import Session

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.negotiation.model import NegotiationCardModel
from mlte.spec.model import ConditionModel, PropertyModel, SpecModel
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
)
from mlte.store.artifact.underlying.rdbs.metadata_nc import (
    DBDataDescriptor,
    DBFieldDescriptor,
    DBGoalDescriptor,
    DBLabelDescriptor,
    DBMetricDescriptor,
    DBModelResourcesDescriptor,
    DBNegotiationCard,
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


def create_db_artifact(
    artifact: ArtifactModel,
    artifact_type_obj: DBArtifactType,
    version_id: int,
    session: Session,
) -> typing.Union[DBSpec, DBValidatedSpec, DBNegotiationCard]:
    """Converts an internal model to its corresponding DB object for artifacts."""
    artifact_header = DBArtifactHeader(
        identifier=artifact.header.identifier,
        type=artifact_type_obj,
        timestamp=artifact.header.timestamp,
        version_id=version_id,
    )

    if artifact.header.type == ArtifactType.SPEC:
        # Create a Spec and its internal lists: properties, and inside them, conditions.
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

        # Create the actual objects.
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
            goal_obj = DBGoalDescriptor(
                description=goal.description, metrics=[]
            )
            for metric in goal.metrics:
                metric_obj = DBMetricDescriptor(
                    description=metric.description, baseline=metric.baseline
                )
                goal_obj.metrics.append(metric_obj)
            negotiation_card_obj.sys_goals.append(goal_obj)

        # Create list of data descriptor objects.
        for data_descriptor in negotiation_card.data:
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
            negotiation_card_obj.data_descriptors.append(data_obj)

        return negotiation_card_obj
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact.header.type}"
        )


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

    body: typing.Union[SpecModel, ValidatedSpecModel]
    if artifact_header.type == ArtifactType.SPEC:
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
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)
