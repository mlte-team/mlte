"""
mlte/model/shared.py

Shared model implementation.
"""

from enum import Enum
from typing import List, Optional

from mlte.model.base_model import BaseModel

# -----------------------------------------------------------------------------
# ProblemType
# -----------------------------------------------------------------------------


class ProblemType(str, Enum):
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


class ModelInterfaceDescriptor(BaseModel):
    """A description of the model interface."""

    input: ModelIODescriptor = ModelIODescriptor()
    """The model input specification."""

    output: ModelIODescriptor = ModelIODescriptor()
    """The model output specification."""


class ModelDevelopmentDescriptor(BaseModel):
    """A descriptor for model development considerations."""

    resources: ModelResourcesDescriptor = ModelResourcesDescriptor()
    """A description of model development resource requirements."""


class ModelProductionDescriptor(BaseModel):
    """A descriptor for model production considerations."""

    deployment_platform: Optional[str] = None
    """A description of the platform used to deploy the model into the system."""

    capability_deployment_mechanism: Optional[str] = None
    """A description of how the model capabilities will be made available."""

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
# DataDescriptor (and sub-models)
# -----------------------------------------------------------------------------


class DataClassification(str, Enum):
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


class QASDescriptor(BaseModel):
    """Describes the system-level requirements for the model component. Represents a Quality Attribute Scenario."""

    quality: Optional[str] = None
    """System property that is being evaluated."""

    stimulus: Optional[str] = None
    """The condition that triggers this scenario."""

    source: Optional[str] = None
    """Where the stimulus comes from."""

    environment: Optional[str] = None
    """Set of circumnstances in which the scenario takes place."""

    response: Optional[str] = None
    """Activity that ocurrs as the result of the stimulus."""

    measure: Optional[str] = None
    """Used to determine if the goals of the responses of the scenario have been achieved."""
