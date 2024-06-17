"""
mlte/store/artifact/underlying/rdbs/factory_value.py

Conversions between schema and internal models.
"""
from __future__ import annotations

import json

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_spec import DBEvidenceMetadata
from mlte.store.artifact.underlying.rdbs.metadata_value import DBValue
from mlte.value.model import ValueModel, ValueType, get_model_class

# -------------------------------------------------------------------------
# Value Factory Methods
# -------------------------------------------------------------------------


def create_value_db_from_model(
    value: ValueModel, artifact_header: DBArtifactHeader
) -> DBValue:
    """Creates the DB object from the corresponding internal model."""
    value_obj = DBValue(
        artifact_header=artifact_header,
        evidence_metadata=DBEvidenceMetadata(
            identifier=str(value.metadata.identifier),
            measurement_type=value.metadata.measurement_type,
            info=value.metadata.info,
        ),
        value_class=value.value_class,
        value_type=value.value.value_type.value,
        data_json=json.dumps(value.value.to_json()),
    )
    return value_obj


def create_value_model_from_db(value_obj: DBValue) -> ValueModel:
    """Creates the internal model object from the corresponding DB object."""
    body = ValueModel(
        metadata=EvidenceMetadata(
            measurement_type=value_obj.evidence_metadata.measurement_type,
            identifier=Identifier(name=value_obj.evidence_metadata.identifier),
        ),
        value_class=value_obj.value_class,
        value=get_model_class(ValueType(value_obj.value_type)).from_json(
            json.loads(value_obj.data_json)
        ),
    )
    return body
