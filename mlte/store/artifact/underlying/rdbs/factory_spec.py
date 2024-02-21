"""
mlte/store/artifact/underlying/rdbs/factory_spec.py

Conversions between schema and internal models.
"""
from __future__ import annotations

import json

from sqlalchemy.orm import Session

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.spec.model import ConditionModel, PropertyModel, SpecModel
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_spec import (
    DBCondition,
    DBEvidenceMetadata,
    DBProperty,
    DBResult,
    DBSpec,
    DBValidatedSpec,
)
from mlte.store.artifact.underlying.rdbs.reader import DBReader
from mlte.validation.model import ResultModel, ValidatedSpecModel

# -------------------------------------------------------------------------
# Spec Factory Methods
# -------------------------------------------------------------------------


def create_spec_db_from_model(
    spec: SpecModel, artifact_header: DBArtifactHeader
) -> DBSpec:
    """Creates the DB object from the corresponding internal model."""
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
                arguments=json.dumps(condition.arguments),
                callback=condition.callback,
                value_class=condition.value_class,
                property=property_obj,
            )
            property_obj.conditions.append(condition_obj)

    return spec_obj


def create_spec_model_from_db(spec_obj: DBSpec) -> SpecModel:
    """Creates the internal model object from the corresponding DB object."""
    # Creating a Spec from DB data.
    body = SpecModel(
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
                        arguments=json.loads(condition.arguments),
                    )
                    for condition in property.conditions
                },
            )
            for property in spec_obj.properties
        ],
    )
    return body


# -------------------------------------------------------------------------
# ValidatedSpec Factory Methods
# -------------------------------------------------------------------------


def create_v_spec_db_from_model(
    validated_spec: ValidatedSpecModel,
    artifact_header: DBArtifactHeader,
    session: Session,
) -> DBValidatedSpec:
    """Creates the DB object from the corresponding internal model."""
    validated_spec_obj = DBValidatedSpec(
        artifact_header=artifact_header,
        results=[],
        spec=DBReader.get_spec(
            validated_spec.spec_identifier, artifact_header.version_id, session
        )
        if validated_spec.spec_identifier != ""
        else None,
    )
    for property_name, results in validated_spec.results.items():
        for measurement_id, result in results.items():
            result_obj = DBResult(
                measurement_id=measurement_id,
                type=result.type,
                message=result.message,
                property_id=DBReader.get_property_id(
                    property_name,
                    validated_spec.spec_identifier,
                    artifact_header.version_id,
                    session,
                ),
                validated_spec=validated_spec_obj,
                evidence_metadata=DBEvidenceMetadata(
                    identifier=measurement_id,
                    measurement_type=result.metadata.measurement_type,
                    info=result.metadata.info,
                )
                if result.metadata is not None
                else None,
            )
            validated_spec_obj.results.append(result_obj)
    return validated_spec_obj


def create_v_spec_model_from_db(
    validated_obj: DBValidatedSpec,
) -> ValidatedSpecModel:
    """Creates the internal model object from the corresponding DB object."""
    body = ValidatedSpecModel(
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
        spec_identifier=validated_obj.spec.artifact_header.identifier
        if validated_obj.spec is not None
        else "",
        spec=create_spec_model_from_db(validated_obj.spec)
        if validated_obj.spec is not None
        else None,
    )
    return body
