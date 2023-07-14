"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from mlte.artifact import Artifact, ArtifactType
from mlte.serde.json import JsonableDataclass, JsonableEnum


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
        return NegotiationCard()


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


@dataclass
class ModelResourcesDescriptor(JsonableDataclass):
    """A descriptor for model resource requirements."""

    cpu: Optional[str] = None
    """A description of model CPU requirements."""

    gpu: Optional[str] = None
    """A description of model GPU requirements."""

    memory: Optional[str] = None
    """A description of model memory (RAM) requirements."""

    storage: Optional[str] = None
    """A description of model storage requirements."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelResourcesDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        print("ModelResourcesDescriptor")
        print(document)
        cpu = _optional_value("cpu", document)
        gpu = _optional_value("gpu", document)
        memory = _optional_value("memory", document)
        storage = _optional_value("storage", document)
        return ModelResourcesDescriptor(
            cpu=cpu, gpu=gpu, memory=memory, storage=storage
        )


@dataclass
class ModelInputDescriptor(JsonableDataclass):
    """A description of the model input specification."""

    description: Optional[str] = None
    """A textual description of the input specification."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelInputDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = _optional_value("description", document)
        return ModelInputDescriptor(description=description)


@dataclass
class ModelOutputDescriptor(JsonableDataclass):
    """A description of the model output specification."""

    description: Optional[str] = None
    """A textual description of the output specification."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelOutputDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        description = _optional_value("description", document)
        return ModelOutputDescriptor(description=description)


@dataclass
class ModelInterfaceDescriptor(JsonableDataclass):
    """A description of the model interface."""

    input: ModelInputDescriptor = field(default_factory=ModelInputDescriptor)
    """The model input specification."""

    output: ModelOutputDescriptor = field(default_factory=ModelOutputDescriptor)
    """The model output specification."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelInterfaceDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        input = (
            ModelInputDescriptor.from_json(document["input"])
            if "input" in document
            else ModelInputDescriptor()
        )
        output = (
            ModelOutputDescriptor.from_json(document["output"])
            if "output" in document
            else ModelOutputDescriptor()
        )
        return ModelInterfaceDescriptor(input=input, output=output)


@dataclass
class ModelDevelopmentDescriptor(JsonableDataclass):
    """A descriptor for model development considerations."""

    resources: ModelResourcesDescriptor = field(
        default_factory=ModelResourcesDescriptor
    )
    """A description of model development resource requirements."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelDevelopmentDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        resources = (
            ModelResourcesDescriptor.from_json(document["resources"])
            if "resources" in document
            else ModelResourcesDescriptor()
        )
        return ModelDevelopmentDescriptor(resources=resources)


@dataclass
class ModelProductionDescriptor(JsonableDataclass):
    """A descriptor for model production considerations."""

    integration: Optional[str] = None
    """A description of the manner in which the model is integrated with the system."""

    interface: ModelInterfaceDescriptor = field(
        default_factory=ModelInterfaceDescriptor
    )
    """A description of the model interface."""

    resources: ModelResourcesDescriptor = field(
        default_factory=ModelResourcesDescriptor
    )
    """A description of model production resource requirements."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelProductionDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        print("ModelProductionDescriptor")
        print(document)
        integration = _optional_value("integration", document)
        interface = (
            ModelInterfaceDescriptor.from_json(document["interface"])
            if "interface" in document
            else ModelInterfaceDescriptor()
        )
        resources = (
            ModelResourcesDescriptor.from_json(document["resources"])
            if "resources" in document
            else ModelResourcesDescriptor()
        )
        return ModelProductionDescriptor(
            integration=integration, interface=interface, resources=resources
        )


@dataclass
class ModelDescriptor(JsonableDataclass):
    """A descriptor for the model."""

    development: ModelDevelopmentDescriptor = field(
        default_factory=ModelDevelopmentDescriptor
    )
    """A description of model development considerations."""

    production: ModelProductionDescriptor = field(
        default_factory=ModelProductionDescriptor
    )
    """A description of model production considerations."""

    @staticmethod
    def from_json(document: dict[str, Any]) -> ModelDescriptor:
        """
        Deserialize from JSON document.
        :param document: The JSON document
        :return: The deserialized instance
        """
        print("ModelDescriptor")
        print(document)
        development = (
            ModelDevelopmentDescriptor.from_json(document["development"])
            if "development" in document
            else ModelDevelopmentDescriptor()
        )
        production = (
            ModelProductionDescriptor.from_json(document["production"])
            if "production" in document
            else ModelProductionDescriptor()
        )
        return ModelDescriptor(development=development, production=production)


# -----------------------------------------------------------------------------
# Misc. Helpers
# -----------------------------------------------------------------------------


def _optional_value(key: str, document: dict[str, Any]) -> Optional[Any]:
    """
    Extract an optional value from a document.
    :param key: The key that identifies the value
    :param document: The input document
    :return: The value if key is present, else `None`.
    """
    print(document)
    if key in document:
        print(f"Key {key} in document")
    else:
        print(f"Key {key} not in document")
    return document[key] if key in document else None
