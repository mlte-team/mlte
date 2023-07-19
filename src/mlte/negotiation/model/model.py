"""
mlte/negotiation/model/model.py

Model implementation for negotiation card artifact.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal, Optional

from mlte.artifact import ArtifactType
from mlte.model import BaseModel

# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


class ProblemType(Enum):
    """An enumeration over machine learning problem types."""

    CLASSIFICATION = "classification"
    CLUSTERING = "clustering"
    TREND = "trend"
    ALERT = "alert"
    FORECASTING = "forecasting"
    CONTENT_GENERATION = "content_generation"
    BENCHMARKING = "benchmarking"
    GOALS = "goals"
    DETECTION = "detection"
    OTHER = "other"


class MetricDescriptor(BaseModel):
    """A description of a metric that supports a system goal."""

    description: Optional[str] = None
    """A description of the metric."""

    baseline: Optional[str] = None
    """A description of the metric baseline value."""


class GoalDescriptor(BaseModel):
    """A description of a system goal."""

    description: Optional[str] = None
    """A description of the goal."""

    metrics: list[MetricDescriptor] = []
    """A collection of metrics related to the goal."""


class RiskDescriptor(BaseModel):
    """A description of system-level risks."""

    fp: Optional[str] = None
    """A description of risks associated with false-positives."""

    fn: Optional[str] = None
    """A description of risks associated with false-negatives."""

    other: Optional[str] = None
    """A description of risks associated with other failures."""


class SystemDescriptor(BaseModel):
    """A description of the system context."""

    goals: list[GoalDescriptor] = []
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
# Data Subcomponents
# -----------------------------------------------------------------------------


class DataClassification(Enum):
    """An enumeration of data classification levels."""

    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    PII = "pii"
    PHI = "phi"
    OTHER = "other"


class LabelDescriptor(BaseModel):
    """Describes a dataset label."""

    description: Optional[str] = None
    """A description of the label."""

    percentage: Optional[float] = None
    """The relative frequency with which the label occurs in the dataset."""


class FieldDescriptor(BaseModel):
    """Describes a dataset field."""

    name: Optional[str] = None
    """The name of the field."""

    description: Optional[str] = None
    """A description of the field."""

    type: Optional[str] = None
    """A description of the field type."""

    expected_values: Optional[str] = None
    """An example of expected values for the field."""

    missing_values: Optional[str] = None
    """An example of missing values for the field."""

    special_values: Optional[str] = None
    """An example of special values for the field."""


class DataDescriptor(BaseModel):
    """Describes a dataset used in model development."""

    description: Optional[str] = None
    """A description of the dataset."""

    source: Optional[str] = None
    """A description of the data source."""

    classification: Optional[DataClassification] = None
    """A description of the data classification level."""

    access: Optional[str] = None
    """A description of the manner in which this data is accessed."""

    labels: list[LabelDescriptor] = []
    """A description of the labels that appear in the dataset."""

    fields: list[FieldDescriptor] = []
    """A description of the dataset schema."""

    rights: Optional[str] = None
    """A description of the ways in which the data can / cannot be used."""

    policies: Optional[str] = None
    """A description of the policies that govern use of this data."""

    identifiable_information: Optional[str] = None
    """A description of personaly-identifiable information considerations for this dataset."""


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


class ModelResourcesDescriptor(BaseModel):
    """A descriptor for model resource requirements."""

    cpu: Optional[str] = None
    """A description of model CPU requirements."""

    gpu: Optional[str] = None
    """A description of model GPU requirements."""

    memory: Optional[str] = None
    """A description of model memory (RAM) requirements."""

    storage: Optional[str] = None
    """A description of model storage requirements."""


class ModelInputDescriptor(BaseModel):
    """A description of the model input specification."""

    description: Optional[str] = None
    """A textual description of the input specification."""


class ModelOutputDescriptor(BaseModel):
    """A description of the model output specification."""

    description: Optional[str] = None
    """A textual description of the output specification."""


class ModelInterfaceDescriptor(BaseModel):
    """A description of the model interface."""

    input: ModelInputDescriptor = ModelInputDescriptor()
    """The model input specification."""

    output: ModelOutputDescriptor = ModelOutputDescriptor()
    """The model output specification."""


class ModelDevelopmentDescriptor(BaseModel):
    """A descriptor for model development considerations."""

    resources: ModelResourcesDescriptor = ModelResourcesDescriptor()
    """A description of model development resource requirements."""


class ModelProductionDescriptor(BaseModel):
    """A descriptor for model production considerations."""

    integration: Optional[str] = None
    """A description of the manner in which the model is integrated with the system."""

    interface: ModelInterfaceDescriptor = ModelInterfaceDescriptor()
    """A description of the model interface."""

    resources: ModelResourcesDescriptor = ModelResourcesDescriptor()
    """A description of model production resource requirements."""


class ModelDescriptor(BaseModel):
    """A descriptor for the model."""

    development: ModelDevelopmentDescriptor = ModelDevelopmentDescriptor()
    """A description of model development considerations."""

    production: ModelProductionDescriptor = ModelProductionDescriptor()
    """A description of model production considerations."""


# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


class NegotiationCardHeaderModel(BaseModel):
    """The NegotiationCardHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the artifact."""

    type: Literal[ArtifactType.NEGOTIATION_CARD]
    """The type identfier for the artifact."""


class NegotiationCardBodyModel(BaseModel):
    """The NegotiationCardBodyModel contains the artifact-specific data for NegotiationCard."""

    system: SystemDescriptor = SystemDescriptor()
    """The descriptor for the system in which the model is integrated."""

    data: list[DataDescriptor] = []
    """A collection of descriptors for relevant data."""

    model: ModelDescriptor = ModelDescriptor()
    """The descriptor for the model."""


class NegotiationCardModel(BaseModel):
    """The model implementation for the NegotiationCard artifact."""

    header: NegotiationCardHeaderModel
    """The model header."""

    body: NegotiationCardBodyModel
    """The model body."""
