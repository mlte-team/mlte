"""
mlte/report/artifact.py

Artifact implementation for MLTE report.
"""

from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import mlte.store.error as errors
from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.shared import DataDescriptor, RiskDescriptor
from mlte.negotiation.artifact import NegotiationCard
from mlte.report.model import (
    CommentDescriptor,
    IntendedUseDescriptor,
    PerformanceDesciptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
    SummaryDescriptor,
)
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession

DEFAULT_REPORT_ID = "default.report"


class Report(Artifact):
    """The report artifact contains the results of MLTE model evaluation."""

    def __init__(
        self,
        identifier: str = DEFAULT_REPORT_ID,
        summary: SummaryDescriptor = SummaryDescriptor(),
        performance: PerformanceDesciptor = PerformanceDesciptor(),
        intended_use: IntendedUseDescriptor = IntendedUseDescriptor(),
        risks: RiskDescriptor = RiskDescriptor(),
        data: List[DataDescriptor] = [],
        comments: List[CommentDescriptor] = [],
        quantitative_analysis: QuantitiveAnalysisDescriptor = QuantitiveAnalysisDescriptor(),
    ) -> None:
        super().__init__(identifier, ArtifactType.REPORT)

        self.summary = summary
        """A summary of the evaluation."""

        self.performance = performance
        """A summary of model performance evaluation."""

        self.intended_use = intended_use
        """The intended use of the model under evaluation."""

        self.risks = risks
        """A description of the risks for the model."""

        self.data = data
        """A description of the data used during model evaluation."""

        self.comments = comments
        """A collection of comments for the report."""

        self.quantitative_analysis = quantitative_analysis
        """The quantitative analysis for the evaluation."""

    def to_model(self) -> ArtifactModel:
        """Convert a report artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ReportModel(
                summary=self.summary,
                performance=self.performance,
                intended_use=self.intended_use,
                risks=self.risks,
                data=self.data,
                comments=self.comments,
                quantitative_analysis=self.quantitative_analysis,
            ),
        )

    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.pre_save_hook(). Loads the associated ValidatedSpec details.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        if self.performance.validated_spec_id is None:
            return

        with ManagedArtifactSession(store.session()) as handle:
            try:
                artifact = handle.read_artifact(
                    context.model,
                    context.version,
                    self.performance.validated_spec_id,
                )
            except errors.ErrorNotFound:
                raise RuntimeError(
                    f"Validated specification with identifier {self.performance.validated_spec_id} not found."
                )

        if not artifact.header.type == ArtifactType.VALIDATED_SPEC:
            raise RuntimeError(
                f"Validated specification with identifier {self.performance.validated_spec_id} not found."
            )

    def post_load_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.post_load_hook().
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        super().post_load_hook(context, store)

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Report:
        """Convert a report model to its corresponding artifact."""
        assert model.header.type == ArtifactType.REPORT, "Broken precondition."
        body = typing.cast(ReportModel, model.body)
        return Report(
            identifier=model.header.identifier,
            summary=body.summary,
            performance=body.performance,
            intended_use=body.intended_use,
            risks=body.risks,
            data=body.data,
            comments=body.comments,
            quantitative_analysis=body.quantitative_analysis,
        )

    def populate_from(self, artifact: NegotiationCard) -> Report:
        """
        Populate the contents of a report from a negotiation card.
        :param artifact: The artifact to populate from
        :return: The new report artifact with fields populated
        """
        summary = deepcopy(self.summary)
        summary.problem_type = artifact.system.problem_type
        summary.task = artifact.system.task

        performance = deepcopy(self.performance)
        performance.goals = artifact.system.goals

        intended_use = deepcopy(self.intended_use)
        intended_use.usage_context = artifact.system.usage_context
        intended_use.production_requirements = artifact.model.production

        return Report(
            identifier=self.identifier,
            summary=summary,
            performance=performance,
            intended_use=intended_use,
            risks=deepcopy(artifact.system.risks),
            data=deepcopy(artifact.data),
            comments=deepcopy(self.comments),
            quantitative_analysis=deepcopy(self.quantitative_analysis),
        )

    @staticmethod
    def get_default_id() -> str:
        """Get the default identifier for the artifact."""
        return DEFAULT_REPORT_ID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Report):
            return False
        return self._equal(other)
