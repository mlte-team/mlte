"""
The base class for MLTE Evidence extensions.

NOTE: The `ExternalEvidence` implementation in this module should not be
confused with the `Evidence` implementation in the `artifact` module.
The `Evidence` implementation in `artifact` is a proper MLTE artifact, it
should be used for all "internal" types part of the MLTE evidence system.
The `ExternalEvidence` implementation in this module is meant to be extended by users
of MLTE to enrich the evidence system with their own evidence types; it provides
the link between the statically-typed MLTE evidence system and dynamic extensions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import mlte._private.meta as meta
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceType, OpaqueValueModel
from mlte.model.base_model import BaseModel


class ExternalEvidence(Evidence, ABC):
    """The base class for MLTE evidence extensions."""

    def __init__(self):
        """Initialize an instance"""
        super().__init__()

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Evidence subclasses."""
        return meta.has_callables(subclass, "serialize", "deserialize")

    @abstractmethod
    def serialize(self) -> dict[str, Any]:
        """
        Serialize the Evidence to a JSON-compatible dictionary.
        :return: The dictionary representation
        """
        raise NotImplementedError("ExternalEvidence.serialize()")

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict[str, Any]) -> ExternalEvidence:
        """
        Deserialize an Evidence instance from serialized representation.
        :param data: The serialized representation
        :return: The deserialized         :param metadata: Evidence metadata associated with the evidence

        """
        raise NotImplementedError("ExternalEvidence.deserialize()")

    def __str__(self) -> str:
        """Return a string representation of this Evidence."""
        return f"{self.serialize()}"

    def to_model(self) -> ArtifactModel:
        """
        Serialize an Evidence to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=OpaqueValueModel(data=self.serialize())
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> ExternalEvidence:
        """
        Deserialize an Evidence from its corresponding model.
        :param model: The artifact model
        :return: The deserialized artifact
        """
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.body.artifact_type == ArtifactType.EVIDENCE
        ), "Broken precondition."
        assert (
            model.body.value.evidence_type == EvidenceType.OPAQUE
        ), "Broken precondition."
        return cls.deserialize(model.body.value.data).with_metadata(
            model.body.metadata
        )
