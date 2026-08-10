"""Model implementation for negotiation card artifact."""

from __future__ import annotations

from typing import Literal

from mlte.artifact.type import ArtifactType
from mlte.model.base_model import BaseModel
from mlte.negotiation import qas

# -----------------------------------------------------------------------------
# GoalDescriptor (and sub-models)
# -----------------------------------------------------------------------------


class MetricDescriptor(BaseModel):
    """A description of a metric that supports a system goal."""

    description: str | None = None
    """A description of the metric."""

    baseline: str | None = None
    """A description of the metric baseline value."""


class GoalDescriptor(BaseModel):
    """A description of a system goal."""

    description: str | None = None
    """A description of the goal."""

    metrics: list[MetricDescriptor] = []
    """A collection of metrics related to the goal."""


# -----------------------------------------------------------------------------
# ModelDescriptor (and sub-models)
# -----------------------------------------------------------------------------


class ModelResourcesDescriptor(BaseModel):
    """A descriptor for model resource requirements."""

    cpu: str | None = None
    """A description of model CPU requirements."""

    gpu: str | None = None
    """A description of model GPU requirements."""

    gpu_memory: str | None = None
    """A description of model GPU memory requirements."""

    main_memory: str | None = None
    """A description of model memory (RAM) requirements."""

    storage: str | None = None
    """A description of model storage requirements."""


class ModelIODescriptor(BaseModel):
    """A description of the model input or output specification."""

    name: str | None = None
    """A name for the input or output."""

    description: str | None = None
    """A textual description of the input or output."""

    type: str | None = None
    """A description of the type of data for this input or output."""

    expected_values: str | None = None
    """Expected values for this input or output."""


class ModelDescriptor(BaseModel):
    """A descriptor for the model."""

    development_compute_resources: ModelResourcesDescriptor = (
        ModelResourcesDescriptor()
    )
    """A description of model development resource requirements."""

    deployment_platform: str | None = None
    """A description of the platform used to deploy the model into the system."""

    capability_deployment_mechanism: str | None = None
    """A description of how the model capabilities will be made available."""

    model_source: str | None = None
    """A description of where the model came from."""

    input_specification: list[ModelIODescriptor] = []
    """The model input specification."""

    output_specification: list[ModelIODescriptor] = []
    """The model output specification."""

    production_compute_resources: ModelResourcesDescriptor = (
        ModelResourcesDescriptor()
    )
    """A description of model production resource requirements."""


# -----------------------------------------------------------------------------
# DataDescriptor (and sub-models)
# -----------------------------------------------------------------------------


class LabelDescriptor(BaseModel):
    """Describes a dataset label."""

    name: str | None = None
    """The name of the label."""

    description: str | None = None
    """A description of the label."""

    percentage: float | None = None
    """The relative frequency with which the label occurs in the dataset."""


class FieldDescriptor(BaseModel):
    """Describes a dataset field."""

    name: str | None = None
    """The name of the field."""

    description: str | None = None
    """A description of the field."""

    type: str | None = None
    """A description of the field type."""

    expected_values: str | None = None
    """An example of expected values for the field."""

    missing_values: str | None = None
    """An example of missing values for the field."""

    special_values: str | None = None
    """An example of special values for the field."""


class DataDescriptor(BaseModel):
    """Describes a dataset used in model development."""

    description: str | None = None
    """A description of the dataset."""

    purpose: str | None = None
    """A description of the purpose of the dataset."""

    source: str | None = None
    """A description of the data source."""

    classification: str = ""
    """A description of the data classification level. Selected from classification custom list."""

    access: str | None = None
    """A description of the manner in which this data is accessed."""

    labeling_method: str | None = None
    """A description of how the data was labeled."""

    labels: list[LabelDescriptor] = []
    """A description of the labels that appear in the dataset."""

    fields: list[FieldDescriptor] = []
    """A description of the dataset schema."""

    rights: str | None = None
    """A description of the ways in which the data can / cannot be used."""

    policies: str | None = None
    """A description of the policies that govern use of this data."""


# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


class SystemDescriptor(BaseModel):
    """A description of the system context."""

    goals: list[GoalDescriptor] = []
    """A description of system goals."""

    problem_type: str = ""
    """A description of the machine learning problem type. Selected from problem types custom list."""

    task: str | None = None
    """A description of the machine learning task."""

    usage_context: str | None = None
    """A description of the usage context."""

    risks: list[str] = []
    """A description of risks associated with system failures."""


# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


class NegotiationCardModel(BaseModel):
    """The model implementation for the NegotiationCard artifact."""

    artifact_type: Literal[ArtifactType.NEGOTIATION_CARD] = (
        ArtifactType.NEGOTIATION_CARD
    )
    """Union discriminator."""

    system: SystemDescriptor = SystemDescriptor()
    """The descriptor for the system in which the model is integrated."""

    data: list[DataDescriptor] = []
    """A collection of descriptors for relevant data."""

    model: ModelDescriptor = ModelDescriptor()
    """The descriptor for the model."""

    system_requirements: list[qas.QASDescriptor] = []
    """The descriptor of the system-level quality requirements."""
