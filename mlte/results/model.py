"""
mlte/validation/model.py

Model implementation for the TestResults artifact.
"""

from typing import Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel
from mlte.tests.model import TestSuiteModel


class ResultModel(BaseModel):
    """A description of a Result."""

    type: str
    """The type of result."""

    message: str
    """The message indicating the reason for status."""

    evidence_metadata: Optional[EvidenceMetadata]
    """Metadata about the evidence this came from."""


class TestResultsModel(BaseModel):
    """The model implementation for the TestResults artifact."""

    artifact_type: Literal[ArtifactType.TEST_RESULTS] = (
        ArtifactType.TEST_RESULTS
    )

    """Union discriminator."""

    test_suite_id: str = ""
    """The identifier of the TestSuite this TestResults came from."""

    test_suite: TestSuiteModel
    """A link to the actual TestSuite details."""

    results: dict[str, ResultModel] = {}
    """A list of validation results, for each test case."""


TestResultsModel.model_rebuild()
