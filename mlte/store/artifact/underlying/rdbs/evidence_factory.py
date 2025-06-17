"""Conversions between schema and internal models."""

from __future__ import annotations

import typing

from mlte._private.fixed_json import json
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.model import EvidenceModel, EvidenceType, get_model_class
from mlte.measurement.model import MeasurementMetadata
from mlte.store.artifact.underlying.rdbs.evidence_metadata import (
    DBEvidence,
    DBEvidenceMetadata,
)
from mlte.store.artifact.underlying.rdbs.main_metadata import DBArtifact

# -------------------------------------------------------------------------
# Evidence Factory Methods
# -------------------------------------------------------------------------


def create_evidence_orm(
    evidence: EvidenceModel, artifact: DBArtifact
) -> DBEvidence:
    """Creates the DB object from the corresponding internal model."""
    value_orm = DBEvidence(
        artifact=artifact,
        evidence_metadata=DBEvidenceMetadata(
            test_case_id=evidence.metadata.test_case_id,
            measurement=json.dumps(evidence.metadata.measurement.to_json()),
        ),
        evidence_class=evidence.evidence_class,
        evidence_type=evidence.value.evidence_type.value,
        data_json=json.dumps(evidence.value.to_json()),
    )
    return value_orm


def create_evidence_model(evidence_orm: DBEvidence) -> EvidenceModel:
    """Creates the internal model object from the corresponding DB object."""
    body = EvidenceModel(
        metadata=EvidenceMetadata(
            test_case_id=evidence_orm.evidence_metadata.test_case_id,
            measurement=typing.cast(
                MeasurementMetadata,
                MeasurementMetadata.from_json(
                    json.loads(evidence_orm.evidence_metadata.measurement)
                ),
            ),
        ),
        evidence_class=evidence_orm.evidence_class,
        value=get_model_class(
            EvidenceType(evidence_orm.evidence_type)
        ).from_json(json.loads(evidence_orm.data_json)),
    )
    return body
