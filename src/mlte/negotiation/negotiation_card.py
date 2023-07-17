"""
mlte/negotiation/negotiation_card.py

Negotiation card artifact implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from mlte.artifact import Artifact, ArtifactType
from mlte.serde.json import JsonableDataclass


@dataclass
class NegotiationCard(Artifact):
    """The negotiation card contains information produced at MLTE negotiation points."""

    def __init__(
        self,
        identifier: str,
    ) -> None:
        super().__init__(identifier, ArtifactType.NEGOTIATION_CARD)


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
    return document[key] if key in document else None
