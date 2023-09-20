"""
mlte/report/model.py

Model implementation for MLTE report.
"""

from typing import List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.model.shared import (
    DataDescriptor,
    GoalDescriptor,
    ModelProductionDescriptor,
    ProblemType,
    RiskDescriptor,
)


class SummaryDescriptor(BaseModel):
    """The model implementation for the report summary."""

    problem_type: Optional[ProblemType] = None
    """The ML problem type."""

    task: Optional[str] = None
    """The ML task."""


class PerformanceDesciptor(BaseModel):
    """The model implementation for the performance descriptor."""

    goals: List[GoalDescriptor] = []
    """A list of the goals for the system."""

    # TODO(Kyle): Implement this.
    findings: Optional[str] = None
    """The findings from MLTE evaluation."""


class IntendedUseDescriptor(BaseModel):
    """The model implementation for intended use."""

    usage_context: Optional[str] = None
    """The intended useage context."""

    production_requirements: ModelProductionDescriptor = (
        ModelProductionDescriptor()
    )
    """The production requirements and considerations for the model."""


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

    artifact_type: Literal[ArtifactType.REPORT]
    """Union discriminator."""

    summary: SummaryDescriptor = SummaryDescriptor()
    """A summary of the model under evaluation."""

    performance: PerformanceDesciptor = PerformanceDesciptor()
    """The results of MLTE model evaluation."""

    intended_use: IntendedUseDescriptor = IntendedUseDescriptor()
    """A description of the intended use of the model."""

    risks: RiskDescriptor = RiskDescriptor()
    """A description of the risks from the system."""

    data: List[DataDescriptor] = []
    """A description of the data used during model training and evaluation."""

    comments: List[CommentDescriptor] = []
    """Comments included in the report."""

    quantitative_analysis: QuantitiveAnalysisDescriptor = (
        QuantitiveAnalysisDescriptor()
    )
    """Quantitative analysis included in the report."""
