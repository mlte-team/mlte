"""Factory to create Evidence artifacts from models."""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType
from mlte.evidence.types.array import Array
from mlte.evidence.types.image import Image
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.opaque import Opaque
from mlte.evidence.types.real import Real
from mlte.evidence.types.string import String


class EvidenceFactory:

    @staticmethod
    def from_model(artifact_model: ArtifactModel) -> Evidence:
        """Returns a proper artifact from the given model."""
        evidence_model = typing.cast(EvidenceModel, artifact_model.body)
        evidence_type = evidence_model.value.evidence_type
        if evidence_type == EvidenceType.INTEGER:
            return Integer.from_model(artifact_model)
        if evidence_type == EvidenceType.REAL:
            return Real.from_model(artifact_model)
        if evidence_type == EvidenceType.IMAGE:
            return Image.from_model(artifact_model)
        if evidence_type == EvidenceType.ARRAY:
            return Array.from_model(artifact_model)
        if evidence_type == EvidenceType.STRING:
            return String.from_model(artifact_model)
        if evidence_type == EvidenceType.OPAQUE:
            return Opaque.from_model(artifact_model)

        raise RuntimeError(f"Evidence type {evidence_type} not supported.")
