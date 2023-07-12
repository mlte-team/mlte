"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel

from mlte.artifact import Artifact, ArtifactType
from mlte.context import Context
from mlte.serde.error import DeserializationError
from mlte.serde.json import JsonableDataclass
from mlte.session import session


@dataclass
class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str,
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)

        self.system: SystemDescriptor = field(default_factory=SystemDescriptor)
        """A description of the system into which the model is integrated."""

        self.data: list[DataDescriptor] = field(default_factory=list)
        """A description of the dataset(s) used to train the model."""

        self.model: ModelDescriptor = field(default_factory=ModelDescriptor)
        """A description of the model itself."""

    def to_json(self) -> dict[str, Any]:
        """
        Serialize a negotiation card artifact to JSON document.
        :return: The serialized document
        """
        return {}

    @staticmethod
    def from_json(document: dict[str, Any]) -> NegotiationCard:
        """
        Deserialize a negotiation card artifact from JSON document.
        :param document: The input document
        :return: The deserialized negotiation card artifact
        """
        pass


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

    def to_json(self) -> dict[str, Any]:
        """
        Serialize to JSON document.
        :return: The JSON document
        """
        return {"value": self.value}

    @staticmethod
    def from_json(document: dict[str, Any]) -> ProblemType:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        _assert_key(document, "value")

        # TODO(Kyle): This is a nice use case for structural pattern matching,
        # but for some reason black cannot yet format this code?
        value = document["value"]
        if value == "classification":
            return ProblemType.CLASSIFICATION
        if value == "clustering":
            return ProblemType.CLUSTERING
        if value == "trend":
            return ProblemType.TREND
        if value == "alert":
            return ProblemType.ALERT
        if value == "forecasting":
            return ProblemType.FORECASTING
        if value == "content_generation":
            return ProblemType.CONTENT_GENERATION
        if value == "benchmarking":
            return ProblemType.BENCHMARKING
        if value == "goals":
            return ProblemType.GOALS
        if value == "detection":
            return ProblemType.DETECTION
        if value == "other":
            return ProblemType.OTHER
        raise RuntimeError(f"Unrecognized problem type: '{document['value']}'.")


@dataclass
class MetricDescriptor(JsonableDataclass):
    """A description of a metric that supports a system goal."""

    description: Optional[str] = None
    """A description of the metric."""

    baseline: Optional[str] = None
    """A description of the metric baseline value."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> MetricDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = (
            document["description"] if "description" in document else None
        )
        baseline = document["baseline"] if "baseline" in document else None
        return MetricDescriptor(description=description, baseline=baseline)


class GoalDescriptor(JsonableDataclass):
    """A description of a system goal."""

    description: Optional[str] = None
    """A description of the goal."""

    metrics: list[MetricDescriptor] = field(default_factory=list)
    """A collection of metrics related to the goal."""


class RiskDescriptor:
    """A description of system-level risks."""

    fp: str
    """A description of risks associated with false-positives."""

    fn: str
    """A description of risks associated with false-negatives."""

    other: str
    """A description of risks associated with other failures."""


@dataclass
class SystemDescriptor(JsonableDataclass):
    """A description of the system context."""

    goals: list[GoalDescriptor] = field(default_factory=list)
    """A description of system goals."""

    problem_type: ProblemType = field(default_factory=ProblemType)
    """A description of the machine learning problem type."""

    task: Optional[str] = None
    """A description of the machine learning task."""

    usage_context: Optional[str] = None
    """A description of the usage context."""

    risks: RiskDescriptor = field(default_factory=RiskDescriptor)
    """A description of risks associated with system failures."""


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


class DataDescriptor:
    """Describes a dataset used in model development."""

    description: str
    """A description of the dataset."""

    source: str
    """A description of the data source."""

    classification: DataClassification
    """A description of the data classification level."""

    access: str
    """A description of the manner in which this data is accessed."""

    labels: list[DataLabelDescriptor]
    """A description of the labels that appear in the dataset."""

    fields: list[DataFieldDescriptor]
    """A description of the dataset schema."""

    rights: str
    """A description of the ways in which the data can / cannot be used."""

    policies: str
    """A description of the policies that govern use of this data."""

    identifiable_information: str
    """A description of personaly-identifiable information considerations for this dataset."""


class DataClassification(Enum):
    """An enumeration of data classification levels."""

    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    PII = "pii"
    PHI = "phi"
    OTHER = "other"


class DataLabelDescriptor:
    """Describes a dataset label."""

    description: str
    """A description of the label."""

    percentage: float
    """The relative frequency with which the label occurs in the dataset."""


class DataFieldDescriptor:
    """Describes a dataset field."""

    name: str
    """The name of the field."""

    description: str
    """A description of the field."""

    type: str
    """A description of the field type."""

    expected_values: str
    """An example of expected values for the field."""

    missing_values: str
    """An example of missing values for the field."""

    special_values: str
    """An example of special values for the field."""


# -----------------------------------------------------------------------------
# Model Subcomponents
# -----------------------------------------------------------------------------


class ModelDescriptor:
    """A descriptor for the model."""


class ModelDevelopmentDescriptor:
    """A descriptor for model development considerations."""

    resources: ModelResourcesDescriptor
    """A description of model development resource requirements."""


class ModelProductionDescriptor:
    """A descriptor for model production considerations."""

    integration: str
    """A description of the manner in which the model is integrated with the system."""

    interface: ModelInterfaceDescriptor
    """A description of the model interface."""

    resources: ModelResourcesDescriptor
    """A description of model production resource requirements."""


class ModelResourcesDescriptor:
    """A descriptor for model resource requirements."""

    cpu: str
    """A description of model CPU requirements."""

    gpu: str
    """A description of model GPU requirements."""

    memory: str
    """A description of model memory (RAM) requirements."""

    storage: str
    """A description of model storage requirements."""


class ModelInterfaceDescriptor:
    """A description of the model interface."""

    input: ModelInputDescriptor
    """The model input specification."""

    output: ModelOutputDescriptor
    """The model output specification."""


class ModelInputDescriptor:
    """A description of the model input specification."""

    description: str
    """A textual description of the input specification."""


class ModelOutputDescriptor:
    """A description of the model output specification."""

    description: str
    """A textual description of the output specification."""


def _assert_key(document: dict[str, Any], key: str):
    """
    Assert that a key is present in a document; raise if not.
    :param document: The input document
    :param key: The key
    :raises DeserializationError: If the key is missing from `document`
    """
    if key not in document:
        raise DeserializationError(key)
