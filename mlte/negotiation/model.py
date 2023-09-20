"""
mlte/negotiation/model.py

Model implementation for negotiation card artifact.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.model.shared import (
    DataDescriptor,
    GoalDescriptor,
    ModelDescriptor,
    ProblemType,
    RiskDescriptor,
)

# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


class SystemDescriptor(BaseModel):
    """A description of the system context."""

    goals: List[GoalDescriptor] = []
    """A description of system goals."""

    problem_type: Optional[ProblemType] = None
    """A description of the machine learning problem type."""

    task: Optional[str] = None
    """A description of the machine learning task."""

    usage_context: Optional[str] = None
    """A description of the usage context."""

    risks: RiskDescriptor = RiskDescriptor()
    """A description of risks associated with system failures."""


# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


class NegotiationCardModel(BaseModel):
    """The model implementation for the NegotiationCard artifact."""

    artifact_type: Literal[ArtifactType.NEGOTIATION_CARD]
    """Union discriminator."""

    system: SystemDescriptor = SystemDescriptor()
    """The descriptor for the system in which the model is integrated."""

    data: List[DataDescriptor] = []
    """A collection of descriptors for relevant data."""

    model: ModelDescriptor = ModelDescriptor()
    """The descriptor for the model."""
