"""
mlte/report/artifact.py

Artifact implementation for MLTE report.
"""

from __future__ import annotations

import datetime
import typing
from typing import List, Optional

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.base_model import BaseModel
from mlte.negotiation.artifact import NegotiationCard
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import CommentDescriptor, ReportModel
from mlte.results.model import TestResultsModel
from mlte.results.test_results import TestResults
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.model import TestSuiteModel
from mlte.tests.test_suite import TestSuite


class Report(Artifact):
    """The report artifact contains the results of MLTE model evaluation."""

    type = ArtifactType.REPORT
    """Class attribute indicating type."""

    def __init__(
        self,
        identifier: Optional[str] = None,
        negotiation_card_id: str = NegotiationCard.build_full_id(),
        negotiation_card_model: Optional[NegotiationCardModel] = None,
        test_suite_id: str = TestSuite.build_full_id(),
        test_suite_model: Optional[TestSuiteModel] = None,
        test_results_id: str = TestResults.build_full_id(),
        test_results_model: Optional[TestResultsModel] = None,
        comments: List[CommentDescriptor] = [],
    ) -> None:
        """
        Creates a Report.

        :param identifier: The Report id (default value used if not provided).
        :param negotiation_card_id: The id of the negotiation card to use (defaults to default card id).
        :param negotiation_card_model: A NegotiationCardModel object; if None, NegotiationCard from the provided id will be loaded.
        :param test_suite_id: The id of the test suite to use (defaults to default suite id).
        :param test_suite_model: A TestSuiteModel object; if None, TestSuite from the provided id will be loaded.
        :param test_results_id: The id of the test results to use (defaults to default results id).
        :param test_results_model: A TestResultsModel object; if None, TestResults from the provided id will be loaded.
        :param comments: Optional comments to add.
        """
        super().__init__(identifier)

        self.negotiation_card_id = negotiation_card_id
        self.negotiation_card_model = (
            negotiation_card_model
            if negotiation_card_model
            else typing.cast(
                NegotiationCardModel,
                NegotiationCard.load(negotiation_card_id).to_model().body,
            )
        )
        """The Negotiation Card with the requirements."""

        self.test_suite_id = test_suite_id
        self.test_suite_model = (
            test_suite_model
            if test_suite_model
            else typing.cast(
                TestSuiteModel, TestSuite.load(test_suite_id).to_model().body
            )
        )
        """The test suite used to generate these results."""

        self.test_results_id = test_results_id
        self.test_results_model = (
            test_results_model
            if test_results_model
            else typing.cast(
                TestResultsModel,
                TestResults.load(test_results_id).to_model().body,
            )
        )
        """A summary of model performance evaluation."""

        self.comments = comments
        """A collection of comments for the report."""

    def to_model(self) -> ArtifactModel:
        """Convert a report artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ReportModel(
                negotiation_card_id=self.negotiation_card_id,
                negotiation_card=self.negotiation_card_model,
                test_suite_id=self.test_suite_id,
                test_suite=self.test_suite_model,
                test_results_id=self.test_results_id,
                test_results=self.test_results_model,
                comments=self.comments,
            ),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Report:
        """Convert a report model to its corresponding artifact."""
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.REPORT
        ), "Type should be Report."
        body = typing.cast(ReportModel, model.body)
        return Report(
            identifier=model.header.identifier,
            negotiation_card_id=body.negotiation_card_id,
            negotiation_card_model=body.negotiation_card,
            test_suite_id=body.test_suite_id,
            test_suite_model=body.test_suite,
            test_results_id=body.test_results_id,
            test_results_model=body.test_results,
            comments=body.comments,
        )

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> Report:
        """
        Load a Report from the configured global session.
        :param identifier: The identifier for the artifact. If None,
        the default id is used.
        """
        report = super().load(identifier)
        return typing.cast(Report, report)

    # Overriden.
    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.pre_save_hook(). Assigns time-stamped id to report, to ensure all have different ids.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        self.identifier = f"{self.identifier}-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # ----------------------------------------------------------------------------------
    # Helper methods.
    # ----------------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Report):
            return False
        return self._equal(other)
