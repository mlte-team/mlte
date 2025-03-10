"""
mlte/store/artifact/underlying/rdbs/factory_value.py

Conversions between schema and internal models.
"""

from __future__ import annotations

import typing

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.model import EvidenceModel, EvidenceType, get_model_class
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.underlying.rdbs.metadata import DBArtifactHeader
from mlte.store.artifact.underlying.rdbs.metadata_evidence import DBEvidence
from mlte.store.artifact.underlying.rdbs.metadata_spec import DBEvidenceMetadata

# -------------------------------------------------------------------------
# Evidence Factory Methods
# -------------------------------------------------------------------------


def create_evidence_db_from_model(
    evidence: EvidenceModel, artifact_header: DBArtifactHeader
) -> DBEvidence:
    """Creates the DB object from the corresponding internal model."""
    value_obj = DBEvidence(
        artifact_header=artifact_header,
        evidence_metadata=DBEvidenceMetadata(
            test_case_id=evidence.metadata.test_case_id,
            measurement=json.dumps(evidence.metadata.measurement.to_json()),
        ),
        evidence_class=evidence.evidence_class,
        evidence_type=evidence.value.evidence_type.value,
        data_json=json.dumps(evidence.value.to_json()),
    )
    return value_obj


def create_evidence_model_from_db(evidence_obj: DBEvidence) -> EvidenceModel:
    """Creates the internal model object from the corresponding DB object."""
    body = EvidenceModel(
        metadata=EvidenceMetadata(
            test_case_id=evidence_obj.evidence_metadata.test_case_id,
            measurement=typing.cast(
                MeasurementMetadata,
                MeasurementMetadata.from_json(
                    json.loads(evidence_obj.evidence_metadata.measurement)
                ),
            ),
        ),
        evidence_class=evidence_obj.evidence_class,
        value=get_model_class(
            EvidenceType(evidence_obj.evidence_type)
        ).from_json(json.loads(evidence_obj.data_json)),
    )
    return body
