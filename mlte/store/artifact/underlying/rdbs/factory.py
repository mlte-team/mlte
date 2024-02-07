"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.spec.model import ConditionModel, PropertyModel, SpecModel
from mlte.store.artifact.underlying.rdbs.metadata import (
    DBArtifactHeader,
    DBArtifactType,
    DBBase,
    DBCondition,
    DBProperty,
    DBResult,
    DBSpec,
    DBValidatedSpec,
)
from mlte.validation.model import (
    PropertyAndResultsModel,
    ResultModel,
    ValidatedSpecModel,
)


def create_db_artifact(
    artifact: ArtifactModel, artifact_type_obj: DBArtifactType, version_id: int
) -> DBBase:
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
        for property in validated_spec.properties:
            for measurement_id, result in property.results.items():
                result_obj = DBResult(
                    measurement_id=measurement_id,
                    type=result.type,
                    message=result.message,
                    property=property_obj,
                    validated_spec=validated_spec_obj,
                )
                validated_spec_obj.results.append(result_obj)
        return validated_spec_obj
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
            properties=[
                PropertyAndResultsModel(
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
                    results={
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
                    },
                )
                for property in validated_obj.spec.properties
            ]
            if validated_obj.spec is not None
            else [],
        )
    else:
        raise Exception(
            f"Unsupported artifact type for conversion: {artifact_header.type}"
        )

    return ArtifactModel(header=artifact_header, body=body)
