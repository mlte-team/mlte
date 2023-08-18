"""
mlte/value/base.py

The base class for MLTE value extensions.

NOTE: The `Value` implementation in this module (`base`) should not be
confused with the `Value` implementation in the `artifact` module.
The `Value` implementation in `artifact` is a proper MLTE artifact, it
should be used for all "internal" types part of the MLTE value system.
The `Value` implementation in this module is meant to be extended by users
of MLTE to enrich the value system with their own value types; it provides
the link between the statically-typed MLTE value system and dynamic extensions.
"""

from __future__ import annotations

import abc
from typing import Any

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.value.model import OpaqueValueModel, ValueModel, ValueType


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Value(Artifact, metaclass=abc.ABCMeta):
    """The base class for MLTE value extensions."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Value subclasses."""
        return all(
            _has_callable(subclass, method)
            for method in ["serialize", "deserialize"]
        )

    def __init__(self, instance: Value, metadata: EvidenceMetadata) -> None:
        """
        Initialize a MLTE value.
        :param instance: The subclass instance
        :param metadata: Evidence metadata associated with the value
        """
        identifier = f"{metadata.identifier}.value"
        super().__init__(identifier, ArtifactType.VALUE)

        self.metadata = metadata
        """Evidence metadata associated with the value."""

        self.typename: str = type(instance).__name__
        """The type of the value itself."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize the value to a JSON-compatible dictionary.
        :return: The dictionary representation
        """
        raise NotImplementedError("Value.serialize()")

    @classmethod
    def deserialize(
        cls, metadata: EvidenceMetadata, data: dict[str, Any]
    ) -> Value:
        """
        Deserialize a Value instance from serialized representation.
        :param metadata: Evidence metadata associated with the value
        :param data: The serialized representation
        :return: The deserialized value
        """
        raise NotImplementedError("Value.deserialize()")

    def to_model(self) -> ArtifactModel:
        """
        Serialize a value to its corresponding model.
        :return: The artifact model
        """
        return ArtifactModel(
            header=ArtifactHeaderModel(
                identifier=self.identifier, type=self.type
            ),
            body=ValueModel(
                artifact_type=ArtifactType.VALUE,
                metadata=self.metadata,
                value=OpaqueValueModel(
                    value_type=ValueType.OPAQUE, data=self.serialize()
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Value:  # noqa[override]
        """
        Deserialize a value from its corresponding model.
        :param model: The artifact model
        :return: The deserialized artifact
        """
        assert (
            model.body.artifact_type == ArtifactType.VALUE
        ), "Broken precondition."
        assert (
            model.body.value.value_type == ValueType.OPAQUE
        ), "Broken precondition."
        return cls.deserialize(model.body.metadata, model.body.value.data)
