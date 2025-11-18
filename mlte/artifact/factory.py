"""Factory to create artifacts from models."""

from __future__ import annotations

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.factory import EvidenceFactory
from mlte.negotiation.artifact import NegotiationCard
from mlte.report.artifact import Report
from mlte.results.test_results import TestResults
from mlte.tests.test_suite import TestSuite


class ArtifactFactory:

    @staticmethod
    def from_model(artifact_model: ArtifactModel) -> Artifact:
        """Returns a proper artifact from the given model."""
        artifact_type = artifact_model.body.artifact_type
        if artifact_type == ArtifactType.NEGOTIATION_CARD:
            return NegotiationCard.from_model(artifact_model)
        if artifact_type == ArtifactType.TEST_SUITE:
            return TestSuite.from_model(artifact_model)
        if artifact_type == ArtifactType.TEST_RESULTS:
            return TestResults.from_model(artifact_model)
        if artifact_type == ArtifactType.REPORT:
            return Report.from_model(artifact_model)
        if artifact_type == ArtifactType.EVIDENCE:
            return EvidenceFactory.from_model(artifact_model)

        raise RuntimeError(f"Artifact type {artifact_type} not supported.")
