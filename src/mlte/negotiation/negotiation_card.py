"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from mlte.artifact import Artifact, ArtifactType
from mlte.context import Context
from mlte.serde.error import DeserializationError
from mlte.serde.json import JsonableDataclass, JsonableEnum
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


class ProblemType(JsonableEnum):
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


@dataclass
class GoalDescriptor(JsonableDataclass):
    """A description of a system goal."""

    description: Optional[str] = None
    """A description of the goal."""

    metrics: list[MetricDescriptor] = field(default_factory=list)
    """A collection of metrics related to the goal."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> GoalDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = (
            document["description"] if "description" in document else None
        )
        metrics = (
            [MetricDescriptor.from_json(item) for item in document["metrics"]]
            if "metrics" in document
            else []
        )
        return GoalDescriptor(description=description, metrics=metrics)


@dataclass
class RiskDescriptor(JsonableDataclass):
    """A description of system-level risks."""

    fp: Optional[str] = None
    """A description of risks associated with false-positives."""

    fn: Optional[str] = None
    """A description of risks associated with false-negatives."""

    other: Optional[str] = None
    """A description of risks associated with other failures."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> RiskDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        fp = document["fp"] if "fp" in document else None
        fn = document["fn"] if "fn" in document else None
        other = document["other"] if "other" in document else None
        return RiskDescriptor(fp=fp, fn=fn, other=other)


@dataclass
class SystemDescriptor(JsonableDataclass):
    """A description of the system context."""

    goals: list[GoalDescriptor] = field(default_factory=list)
    """A description of system goals."""

    problem_type: Optional[ProblemType] = None
    """A description of the machine learning problem type."""

    task: Optional[str] = None
    """A description of the machine learning task."""

    usage_context: Optional[str] = None
    """A description of the usage context."""

    risks: RiskDescriptor = field(default_factory=RiskDescriptor)
    """A description of risks associated with system failures."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> SystemDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        goals = (
            [GoalDescriptor.from_json(item) for item in document["goals"]]
            if "goals" in document
            else []
        )
        problem_type = (
            ProblemType.from_json(document["problem_type"])
            if "problem_type" in document
            else None
        )
        task = document["task"] if "task" in document else None
        usage_context = (
            document["usage_context"] if "usage_context" in document else None
        )
        risks = (
            RiskDescriptor.from_json(document["risks"])
            if "risks" in document
            else RiskDescriptor()
        )
        return SystemDescriptor(
            goals=goals,
            problem_type=problem_type,
            task=task,
            usage_context=usage_context,
            risks=risks,
        )


# -----------------------------------------------------------------------------
# Data Subcomponents
# -----------------------------------------------------------------------------


class DataClassification(JsonableEnum):
    """An enumeration of data classification levels."""

    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    PII = "pii"
    PHI = "phi"
    OTHER = "other"


@dataclass
class LabelDescriptor(JsonableDataclass):
    """Describes a dataset label."""

    description: Optional[str] = None
    """A description of the label."""

    percentage: Optional[float] = None
    """The relative frequency with which the label occurs in the dataset."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> LabelDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = (
            document["description"] if "description" in document else None
        )
        percentage = (
            document["percentage"] if "percentage" in document else None
        )
        return LabelDescriptor(description=description, percentage=percentage)


@dataclass
class FieldDescriptor(JsonableDataclass):
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

    @staticmethod
    def from_json(document: dict[str, Any]) -> FieldDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        name = document["name"] if "name" in document else None
        description = (
            document["description"] if "description" in document else None
        )
        type = document["type"] if "type" in document else None
        expected_values = (
            document["expected_values"]
            if "expected_values" in document
            else None
        )
        missing_values = (
            document["missing_values"] if "missing_values" in document else None
        )
        special_values = (
            document["special_values"] if "special_values" in document else None
        )
        return FieldDescriptor(
            name=name,
            description=description,
            type=type,
            expected_values=expected_values,
            missing_values=missing_values,
            special_values=special_values,
        )


@dataclass
class DataDescriptor(JsonableDataclass):
    """Describes a dataset used in model development."""

    description: Optional[str] = None
    """A description of the dataset."""

    source: Optional[str] = None
    """A description of the data source."""

    classification: Optional[DataClassification] = None
    """A description of the data classification level."""

    access: Optional[str] = None
    """A description of the manner in which this data is accessed."""

    labels: list[LabelDescriptor] = field(default_factory=list)
    """A description of the labels that appear in the dataset."""

    fields: list[FieldDescriptor] = field(default_factory=list)
    """A description of the dataset schema."""

    rights: Optional[str] = None
    """A description of the ways in which the data can / cannot be used."""

    policies: Optional[str] = None
    """A description of the policies that govern use of this data."""

    identifiable_information: Optional[str] = None
    """A description of personaly-identifiable information considerations for this dataset."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> DataDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = (
            document["description"] if "description" in document else None
        )
        source = document["source"] if "source" in document else None
        classification = (
            DataClassification.from_json(document["classification"])
            if "classification" in document
            else None
        )
        access = document["access"] if "access" in document else None
        labels = (
            [LabelDescriptor.from_json(item) for item in document["labels"]]
            if "labels" in document
            else []
        )
        fields = (
            [FieldDescriptor.from_json(item) for item in document["fields"]]
            if "fields" in document
            else []
        )
        rights = document["rights"] if "rights" in document else None
        policies = document["policies"] if "policies" in document else None
        identifiable_information = (
            document["identifiable_information"]
            if "identifiable_information" in document
            else None
        )
        return DataDescriptor(
            description=description,
            source=source,
            classification=classification,
            access=access,
            labels=labels,
            fields=fields,
            rights=rights,
            policies=policies,
            identifiable_information=identifiable_information,
        )


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
