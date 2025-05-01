"""
mlte/negotiation/model.py

Model implementation for negotiation card artifact.
"""

from __future__ import annotations

from typing import Any, List, Literal, Optional

from strenum import StrEnum

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.negotiation import qas

# -----------------------------------------------------------------------------
# ProblemType
# -----------------------------------------------------------------------------


class ProblemType(StrEnum):
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


# -----------------------------------------------------------------------------
# GoalDescriptor (and sub-models)
# -----------------------------------------------------------------------------


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

    metrics: List[MetricDescriptor] = []
    """A collection of metrics related to the goal."""


# -----------------------------------------------------------------------------
# RiskDescriptor
# -----------------------------------------------------------------------------


class RiskDescriptor(BaseModel):
    """A description of system-level risks."""

    fp: Optional[str] = None
    """A description of risks associated with false-positives."""

    fn: Optional[str] = None
    """A description of risks associated with false-negatives."""

    other: Optional[str] = None
    """A description of risks associated with other failures."""


# -----------------------------------------------------------------------------
# ModelDescriptor (and sub-models)
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


class ModelIODescriptor(BaseModel):
    """A description of the model input or output specification."""

    name: Optional[str] = None
    """A name for the input or output."""

    description: Optional[str] = None
    """A textual description of the input or output."""

    type: Optional[str] = None
    """A description of the type of data for this input or output."""

    expected_values: Optional[str] = None
    """Expected values for this input or output."""


class ModelDescriptor(BaseModel):
    """A descriptor for the model."""

    development_compute_resources: ModelResourcesDescriptor = (
        ModelResourcesDescriptor()
    )
    """A description of model development resource requirements."""

    deployment_platform: Optional[str] = None
    """A description of the platform used to deploy the model into the system."""

    capability_deployment_mechanism: Optional[str] = None
    """A description of how the model capabilities will be made available."""

    input_specification: List[ModelIODescriptor] = []
    """The model input specification."""

    output_specification: List[ModelIODescriptor] = []
    """The model output specification."""

    production_compute_resources: ModelResourcesDescriptor = (
        ModelResourcesDescriptor()
    )
    """A description of model production resource requirements."""


# -----------------------------------------------------------------------------
# DataDescriptor (and sub-models)
# -----------------------------------------------------------------------------


class DataClassification(StrEnum):
    """An enumeration of data classification levels."""

    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    PII = "pii"
    PHI = "phi"
    CLASSIFIED = "classified"
    OTHER = "other"


class LabelDescriptor(BaseModel):
    """Describes a dataset label."""

    name: Optional[str] = None
    """The name of the label."""

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

    labeling_method: Optional[str] = None
    """A description of how the data was labeled."""

    labels: List[LabelDescriptor] = []
    """A description of the labels that appear in the dataset."""

    fields: List[FieldDescriptor] = []
    """A description of the dataset schema."""

    rights: Optional[str] = None
    """A description of the ways in which the data can / cannot be used."""

    policies: Optional[str] = None
    """A description of the policies that govern use of this data."""


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
# NegotiationCardDataModel
# -----------------------------------------------------------------------------


class NegotiationCardDataModel(BaseModel):
    """The model implementation for the NegotiationCard information."""

    system: SystemDescriptor = SystemDescriptor()
    """The descriptor for the system in which the model is integrated."""

    data: List[DataDescriptor] = []
    """A collection of descriptors for relevant data."""

    model: ModelDescriptor = ModelDescriptor()
    """The descriptor for the model."""

    system_requirements: List[qas.QASDescriptor] = []
    """The descriptor of the system-level quality requirements."""


# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


class NegotiationCardModel(BaseModel):
    """The model implementation for the NegotiationCard artifact."""

    artifact_type: Literal[ArtifactType.NEGOTIATION_CARD] = (
        ArtifactType.NEGOTIATION_CARD
    )
    """Union discriminator."""

    nc_data: NegotiationCardDataModel = NegotiationCardDataModel()
    """The specific data for this negotiation card."""

    # Overriden.
    def post_validation_hook(self, data: Optional[Any] = None) -> Any:
        """Called after validation, allows us to generate ids for QASs."""
        if not data or not isinstance(data, str):
            raise RuntimeError(
                f"Invalid data id received in Negotiation Card model: {data}"
            )
        identifier = str(data)
        qas.add_qas_ids(identifier, self.nc_data.system_requirements)
        return self
