"""Model implementation for MLTE report."""

from typing import List, Literal

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.results.model import TestResultsModel
from mlte.tests.model import TestSuiteModel


class CommentDescriptor(BaseModel):
    """The model implementation for a generic comment."""

    content: str
    """The comment content."""


class ReportModel(BaseModel):
    """The model implementation for the MLTE report artifact."""

    artifact_type: Literal[ArtifactType.REPORT] = ArtifactType.REPORT
    """Union discriminator."""

    negotiation_card_id: str
    """The id of the negotiation card we got the information from."""

    negotiation_card: NegotiationCardModel
    """The specific data from a negotiation card."""

    test_suite_id: str
    """The id of the test suite we got the information from."""

    test_suite: TestSuiteModel
    """The TestSuite used for this run."""

    test_results_id: str
    """The id of the test results we got the information from."""

    test_results: TestResultsModel
    """The actual detailed results of the test run."""

    comments: List[CommentDescriptor] = []
    """Comments included in the report."""
