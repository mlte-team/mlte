"""
mlte/report/artifact.py

Artifact implementation for MLTE report.
"""

from __future__ import annotations

import typing
from copy import deepcopy
from typing import List, Optional

import mlte.store.error as errors
from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.model.base_model import BaseModel
from mlte.negotiation.artifact import NegotiationCard
from mlte.negotiation.model import (
    DataDescriptor,
    ModelDescriptor,
    NegotiationCardDataModel,
    SystemDescriptor,
)
from mlte.negotiation.qas import QASDescriptor
from mlte.report.model import (
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
    ReportModel,
)
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession

DEFAULT_REPORT_ID = "default.report"


class Report(Artifact):
    """The report artifact contains the results of MLTE model evaluation."""

    def __init__(
        self,
        identifier: str = DEFAULT_REPORT_ID,
        system: SystemDescriptor = SystemDescriptor(),
        model: ModelDescriptor = ModelDescriptor(),
        data: List[DataDescriptor] = [],
        system_requirements: List[QASDescriptor] = [],
        test_results_id: Optional[str] = None,
        comments: List[CommentDescriptor] = [],
        quantitative_analysis: QuantitiveAnalysisDescriptor = QuantitiveAnalysisDescriptor(),
    ) -> None:
        super().__init__(identifier, ArtifactType.REPORT)

        self.system = system
        """A system requirements."""

        self.data = data
        """A description of the data used during model evaluation."""

        self.model = model
        """The intended use of the model under evaluation."""

        self.system_requirements = system_requirements
        """A description of the system requirements."""

        self.test_results_id = test_results_id
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
                nc_data=NegotiationCardDataModel(
                    system=self.system,
                    data=self.data,
                    model=self.model,
                    system_requirements=self.system_requirements,
                ),
                test_results_id=self.test_results_id,
                comments=self.comments,
                quantitative_analysis=self.quantitative_analysis,
            ),
        )

    def pre_save_hook(self, context: Context, store: ArtifactStore) -> None:
        """
        Override Artifact.pre_save_hook(). Loads the associated TestResults details.
        :param context: The context in which to save the artifact
        :param store: The store in which to save the artifact
        :raises RuntimeError: On broken invariant
        """
        if self.test_results_id is None:
            return

        with ManagedArtifactSession(store.session()) as handle:
            try:
                artifact = handle.read_artifact(
                    context.model,
                    context.version,
                    self.test_results_id,
                )
            except errors.ErrorNotFound:
                raise RuntimeError(
                    f"Test Results with identifier {self.test_results_id} not found."
                )

        if not artifact.header.type == ArtifactType.TEST_RESULTS:
            raise RuntimeError(
                f"Test Results with identifier {self.test_results_id} not found."
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
            system=body.nc_data.system,
            data=body.nc_data.data,
            model=body.nc_data.model,
            system_requirements=body.nc_data.system_requirements,
            test_results_id=body.test_results_id,
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

    def populate_from(self, artifact: NegotiationCard) -> Report:
        """
        Populate the contents of a report from a negotiation card.
        :param artifact: The artifact to populate from
        :return: The new report artifact with fields populated
        """
        return Report(
            identifier=self.identifier,
            system=deepcopy(artifact.system),
            data=deepcopy(artifact.data),
            model=deepcopy(artifact.model),
            system_requirements=deepcopy(artifact.quality_scenarios),
            test_results_id=self.test_results_id,
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
