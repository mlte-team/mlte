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
from mlte.model.shared import (
    DataDescriptor,
    ModelDescriptor,
    NegotiationCardDataModel,
    QASDescriptor,
    SystemDescriptor,
)
from mlte.negotiation.artifact import NegotiationCard
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
        validated_spec_id: Optional[str] = None,
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

        self.validated_spec_id = validated_spec_id
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
                validated_spec_id=self.validated_spec_id,
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
        if self.validated_spec_id is None:
            return

        with ManagedArtifactSession(store.session()) as handle:
            try:
                artifact = handle.read_artifact(
                    context.model,
                    context.version,
                    self.validated_spec_id,
                )
            except errors.ErrorNotFound:
                raise RuntimeError(
                    f"Validated specification with identifier {self.validated_spec_id} not found."
                )

        if not artifact.header.type == ArtifactType.VALIDATED_SPEC:
            raise RuntimeError(
                f"Validated specification with identifier {self.validated_spec_id} not found."
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
            system=body.nc_data.system,
            data=body.nc_data.data,
            model=body.nc_data.model,
            system_requirements=body.nc_data.system_requirements,
            validated_spec_id=body.validated_spec_id,
            comments=body.comments,
            quantitative_analysis=body.quantitative_analysis,
        )

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
            system_requirements=deepcopy(artifact.qas),
            validated_spec_id=self.validated_spec_id,
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
