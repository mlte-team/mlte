"""
mlte/negotiation/model/model.py

Model implementation for negotiation card artifact.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from mlte.artifact.model import BaseModel


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

    risks: Optional[RiskDescriptor] = None
    """A description of risks associated with system failures."""


# # -----------------------------------------------------------------------------
# # Data Subcomponents
# # -----------------------------------------------------------------------------


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


# # -----------------------------------------------------------------------------
# # Model Subcomponents
# # -----------------------------------------------------------------------------


# @dataclass
# class ModelResourcesDescriptor(JsonableDataclass):
#     """A descriptor for model resource requirements."""

#     cpu: Optional[str] = None
#     """A description of model CPU requirements."""

#     gpu: Optional[str] = None
#     """A description of model GPU requirements."""

#     memory: Optional[str] = None
#     """A description of model memory (RAM) requirements."""

#     storage: Optional[str] = None
#     """A description of model storage requirements."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelResourcesDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         print("ModelResourcesDescriptor")
#         print(document)
#         cpu = _optional_value("cpu", document)
#         gpu = _optional_value("gpu", document)
#         memory = _optional_value("memory", document)
#         storage = _optional_value("storage", document)
#         return ModelResourcesDescriptor(
#             cpu=cpu, gpu=gpu, memory=memory, storage=storage
#         )


# @dataclass
# class ModelInputDescriptor(JsonableDataclass):
#     """A description of the model input specification."""

#     description: Optional[str] = None
#     """A textual description of the input specification."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelInputDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         description = _optional_value("description", document)
#         return ModelInputDescriptor(description=description)


# @dataclass
# class ModelOutputDescriptor(JsonableDataclass):
#     """A description of the model output specification."""

#     description: Optional[str] = None
#     """A textual description of the output specification."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelOutputDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         description = _optional_value("description", document)
#         return ModelOutputDescriptor(description=description)


# @dataclass
# class ModelInterfaceDescriptor(JsonableDataclass):
#     """A description of the model interface."""

#     input: ModelInputDescriptor = field(default_factory=ModelInputDescriptor)
#     """The model input specification."""

#     output: ModelOutputDescriptor = field(default_factory=ModelOutputDescriptor)
#     """The model output specification."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelInterfaceDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         input = (
#             ModelInputDescriptor.from_json(document["input"])
#             if "input" in document
#             else ModelInputDescriptor()
#         )
#         output = (
#             ModelOutputDescriptor.from_json(document["output"])
#             if "output" in document
#             else ModelOutputDescriptor()
#         )
#         return ModelInterfaceDescriptor(input=input, output=output)


# @dataclass
# class ModelDevelopmentDescriptor(JsonableDataclass):
#     """A descriptor for model development considerations."""

#     resources: ModelResourcesDescriptor = field(
#         default_factory=ModelResourcesDescriptor
#     )
#     """A description of model development resource requirements."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelDevelopmentDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         resources = (
#             ModelResourcesDescriptor.from_json(document["resources"])
#             if "resources" in document
#             else ModelResourcesDescriptor()
#         )
#         return ModelDevelopmentDescriptor(resources=resources)


# @dataclass
# class ModelProductionDescriptor(JsonableDataclass):
#     """A descriptor for model production considerations."""

#     integration: Optional[str] = None
#     """A description of the manner in which the model is integrated with the system."""

#     interface: ModelInterfaceDescriptor = field(
#         default_factory=ModelInterfaceDescriptor
#     )
#     """A description of the model interface."""

#     resources: ModelResourcesDescriptor = field(
#         default_factory=ModelResourcesDescriptor
#     )
#     """A description of model production resource requirements."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelProductionDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         print("ModelProductionDescriptor")
#         print(document)
#         integration = _optional_value("integration", document)
#         interface = (
#             ModelInterfaceDescriptor.from_json(document["interface"])
#             if "interface" in document
#             else ModelInterfaceDescriptor()
#         )
#         resources = (
#             ModelResourcesDescriptor.from_json(document["resources"])
#             if "resources" in document
#             else ModelResourcesDescriptor()
#         )
#         return ModelProductionDescriptor(
#             integration=integration, interface=interface, resources=resources
#         )


# @dataclass
# class ModelDescriptor(JsonableDataclass):
#     """A descriptor for the model."""

#     development: ModelDevelopmentDescriptor = field(
#         default_factory=ModelDevelopmentDescriptor
#     )
#     """A description of model development considerations."""

#     production: ModelProductionDescriptor = field(
#         default_factory=ModelProductionDescriptor
#     )
#     """A description of model production considerations."""

#     @staticmethod
#     def from_json(document: dict[str, Any]) -> ModelDescriptor:
#         """
#         Deserialize from JSON document.
#         :param document: The JSON document
#         :return: The deserialized instance
#         """
#         print("ModelDescriptor")
#         print(document)
#         development = (
#             ModelDevelopmentDescriptor.from_json(document["development"])
#             if "development" in document
#             else ModelDevelopmentDescriptor()
#         )
#         production = (
#             ModelProductionDescriptor.from_json(document["production"])
#             if "production" in document
#             else ModelProductionDescriptor()
#         )
#         return ModelDescriptor(development=development, production=production)
