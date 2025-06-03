"""
mlte/report/artifact.py

Artifact implementation for MLTE report.
"""

from __future__ import annotations

import datetime
import typing
from typing import List, Optional

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.base_model import BaseModel
from mlte.negotiation.artifact import NegotiationCard
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.results.model import TestResultsModel
from mlte.results.test_results import TestResults
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.model import TestSuiteModel
from mlte.tests.test_suite import TestSuite

DEFAULT_REPORT_ID = "default.report"


class Report(Artifact):
    """The report artifact contains the results of MLTE model evaluation."""

    def __init__(
        self,
        identifier: str = DEFAULT_REPORT_ID,
        negotiation_card: Optional[NegotiationCard] = None,
        test_suite: Optional[TestSuite] = None,
        test_results: Optional[TestResults] = None,
        comments: List[CommentDescriptor] = [],
        quantitative_analysis: QuantitiveAnalysisDescriptor = QuantitiveAnalysisDescriptor(),
    ) -> None:
        """
        Creates a Report.

        :param identifier: The Report id (default value used if not provided).
        :param negotiation_card: A NegotiationCard object; if None, NegotiationCard with default id will be loaded.
        :param test_suite: A TestSuite object; if None, TestSuite with default id will be loaded.
        :param test_results: A TestResults object; if None, TestResults with default id will be loaded.
        :param comments: Optional comments to add.
        :quantitative_analysis: Optional additional analysis to add.
        """
        super().__init__(identifier, ArtifactType.REPORT)

        self.negotiation_card = (
            negotiation_card if negotiation_card else NegotiationCard.load()
        )
        """The Negotiation Card with the requirements."""

        self.test_suite = test_suite if test_suite else TestSuite.load()
        """The test suite used to generate these results."""

        self.test_results = test_results if test_results else TestResults.load()
        """A summary of model performance evaluation."""

        self.comments = comments
        """A collection of comments for the report."""

        self.quantitative_analysis = quantitative_analysis
        """The quantitative analysis for the evaluation."""

    def to_model(self) -> ArtifactModel:
        """Convert a report artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ReportModel(
                negotiation_card_id=self.negotiation_card.identifier,
                negotiation_card=typing.cast(
                    NegotiationCardModel, self.negotiation_card.to_model().body
                ),
                test_suite_id=self.test_suite.identifier,
                test_suite=typing.cast(
                    TestSuiteModel, self.test_suite.to_model().body
                ),
                test_results_id=self.test_results.identifier,
                test_results=typing.cast(
                    TestResultsModel, self.test_results.to_model().body
                ),
                comments=self.comments,
                quantitative_analysis=self.quantitative_analysis,
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
            negotiation_card=NegotiationCard.from_model(
                ArtifactModel(
                    header=ArtifactHeaderModel(
                        identifier=body.negotiation_card_id,
                        type=ArtifactType.NEGOTIATION_CARD,
                    ),
                    body=body.negotiation_card,
                )
            ),
            test_suite=TestSuite.from_model(
                ArtifactModel(
                    header=ArtifactHeaderModel(
                        identifier=body.test_suite_id,
                        type=ArtifactType.TEST_SUITE,
                    ),
                    body=body.test_suite,
                )
            ),
            test_results=TestResults.from_model(
                ArtifactModel(
                    header=ArtifactHeaderModel(
                        identifier=body.test_results_id,
                        type=ArtifactType.TEST_RESULTS,
                    ),
                    body=body.test_results,
                )
            ),
            comments=body.comments,
            quantitative_analysis=body.quantitative_analysis,
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
        self.identifier = f"{self.identifier}-{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}"

    # ----------------------------------------------------------------------------------
    # Helper methods.
    # ----------------------------------------------------------------------------------

    @staticmethod
    def get_default_id() -> str:
        """Get the default identifier for the artifact."""
        return DEFAULT_REPORT_ID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Report):
            return False
        return self._equal(other)
