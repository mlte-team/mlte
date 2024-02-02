"""
mlte/store/artifact/underlying/rdbs/factory.py

Creation of metadata objects from pydantic models.
"""

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.spec.model import SpecModel
from mlte.store.artifact.underlying.rdbs.metadata import (
    Base,
    DBArtifactHeader,
    DBArtifactType,
    DBCondition,
    DBProperty,
    DBSpec,
)


def create_db_artifact(
    artifact: ArtifactModel, artifact_type_obj: DBArtifactType
) -> Base:
    """Converts an internal model to its corresponding DB object for artifacts."""
    artifact_header = DBArtifactHeader(
        identifier=artifact.header.identifier,
        type=artifact_type_obj,
        timestamp=artifact.header.timestamp,
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
    else:
        raise Exception(f"Unsupported artifact: {artifact.header.type}")
