"""
mlte/store/artifact/underlying/rdbs/factory_value.py

Conversions between schema and internal models.
"""

from __future__ import annotations

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.model import EvidenceModel, EvidenceType, get_model_class
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_spec import DBEvidenceMetadata
from mlte.store.artifact.underlying.rdbs.metadata_value import DBValue

# -------------------------------------------------------------------------
# Value Factory Methods
# -------------------------------------------------------------------------


def create_value_db_from_model(
    value: EvidenceModel, artifact_header: DBArtifactHeader
) -> DBValue:
    """Creates the DB object from the corresponding internal model."""
    value_obj = DBValue(
        artifact_header=artifact_header,
        evidence_metadata=DBEvidenceMetadata(
            identifier=str(value.metadata.test_case_id),
            measurement_type=value.metadata.measurement.measurement_class,
            info=value.metadata.measurement.additional_data,
        ),
        value_class=value.evidence_class,
        value_type=value.value.value_type.value,
        data_json=json.dumps(value.value.to_json()),
    )
    return value_obj


def create_value_model_from_db(value_obj: DBValue) -> EvidenceModel:
    """Creates the internal model object from the corresponding DB object."""
    body = EvidenceModel(
        metadata=EvidenceMetadata(
            test_case_id=value_obj.evidence_metadata.identifier,
            measurement=MeasurementMetadata(
                measurement_class=value_obj.evidence_metadata.measurement_type,
            ),
        ),
        evidence_class=value_obj.value_class,
        value=get_model_class(EvidenceType(value_obj.value_type)).from_json(
            json.loads(value_obj.data_json)
        ),
    )
    return body
