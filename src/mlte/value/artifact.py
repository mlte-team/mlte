"""
mlte/value/artifact.py

Artifact implementation for MLTE values.
"""

from __future__ import annotations

import abc

from mlte.artifact.artifact import Artifact
from mlte.evidence.metadata import EvidenceMetadata
from mlte.artifact.model import ArtifactType, ArtifactModel


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Value(Artifact, metaclass=abc.ABCMeta):
    """
    The Value class serves as the base class of all
    semantically-enriched measurement evaluation values.
    The Value provides a common interface for inspecting
    the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all Value subclasses."""
        return all(
            _has_callable(subclass, method)
            for method in ["to_model", "from_model"]
        )

    def __init__(self, instance: Value, metadata: EvidenceMetadata):
        """
        Initialize a Value instance.
        :param instance: The subclass instance
        :param metadata: Evidence metadata associated with the value
        """
        # TODO(Kyle): How is this identifier constructed?
        identifier = f"{metadata.identifier}.value"
        super().__init__(identifier, ArtifactType.VALUE)

        self.metadata = metadata
        """Evidence metadata associated with the value."""

        self.typename: str = type(instance).__name__
        """The type of the value itself."""

    def to_model(self) -> ArtifactModel:
        """
        Convert a value artifact to its corresponding model.
        NOTE: To cope with polymorphism, the Value artifact type
        does not define this required method itself; instead, it
        is delegated to subclasses that implement concrete types
        """
        raise NotImplementedError("Value.to_mode()")

    @staticmethod
    def from_model(model: ArtifactModel) -> Value:  # type: ignore[override]
        """
        Convert a value model to its corresponding artifact.
        NOTE: To cope with polymorphism, the Value artifact type
        does not define this required method itself; instead, it
        is delegated to subclasses that implement concrete types
        """
        raise NotImplementedError("Value.from_model()")
