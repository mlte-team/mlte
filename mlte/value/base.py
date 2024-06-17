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
from typing import Any, Dict

import mlte._private.meta as meta
import mlte.value.artifact as artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.value.model import OpaqueValueModel, ValueModel, ValueType


class ValueBase(artifact.Value, metaclass=abc.ABCMeta):
    """The base class for MLTE value extensions."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Value subclasses."""
        return meta.has_callables(subclass, "serialize", "deserialize")

    @abc.abstractmethod
    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the value to a JSON-compatible dictionary.
        :return: The dictionary representation
        """
        raise NotImplementedError("ValueBase.serialize()")

    @classmethod
    @abc.abstractmethod
    def deserialize(
        cls, metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> ValueBase:
        """
        Deserialize a Value instance from serialized representation.
        :param metadata: Evidence metadata associated with the value
        :param data: The serialized representation
        :return: The deserialized value
        """
        raise NotImplementedError("ValueBase.deserialize()")

    def to_model(self) -> ArtifactModel:
        """
        Serialize a value to its corresponding model.
        :return: The artifact model
        """
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ValueModel(
                metadata=self.metadata,
                value_class=self.get_class_path(),
                value=OpaqueValueModel(
                    data=self.serialize(),
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> ValueBase:  # noqa[override]
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
