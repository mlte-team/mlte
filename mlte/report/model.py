"""
mlte/report/model.py

Model implementation for MLTE report.
"""

from typing import List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.model.shared import NegotiationCardDataModel


class CommentDescriptor(BaseModel):
    """The model implementation for a generic comment."""

    content: str
    """The comment content."""


class QuantitiveAnalysisDescriptor(BaseModel):
    """The model implementation for report quantitative analysis."""

    # TODO(Kyle): This is not implemented.
    content: Optional[str] = None
    """The field content."""


class ReportModel(BaseModel):
    """The model implementation for the MLTE report artifact."""

    artifact_type: Literal[ArtifactType.REPORT] = ArtifactType.REPORT
    """Union discriminator."""

    nc_data: NegotiationCardDataModel = NegotiationCardDataModel()
    """The specific data from a negotiation card."""

    validated_spec_id: Optional[str] = None
    """The findings from MLTE evaluation."""

    comments: List[CommentDescriptor] = []
    """Comments included in the report."""

    quantitative_analysis: QuantitiveAnalysisDescriptor = (
        QuantitiveAnalysisDescriptor()
    )
    """Quantitative analysis included in the report."""
