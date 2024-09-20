"""
mlte/value/artifact.py

Artifact implementation for MLTE values.
"""

from __future__ import annotations

import abc
import typing

from mlte._private.meta import get_class_path
from mlte._private.reflection import load_class
from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata
from mlte.store.artifact.store import ArtifactStore
from mlte.value.model import ValueModel


class Value(Artifact, metaclass=abc.ABCMeta):
    """
    The Value class serves as the base class of all
    semantically-enriched measurement evaluation values.
    The Value provides a common interface for inspecting
    the results of measurement evaluation, and also
    encapsulates the functionality required to uniquely
    associate evaluation results with the originating measurement.
    """

    def __init__(self, instance: Value, metadata: EvidenceMetadata):
        """
        Initialize a Value instance.
        :param instance: The subclass instance
        :param metadata: Evidence metadata associated with the value
        """
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

    @classmethod
    def from_model(cls, _: ArtifactModel) -> Value:
        """
        Convert a value model to its corresponding artifact.
        NOTE: To cope with polymorphism, the Value artifact type
        does not define this required method itself; instead, it
        is delegated to subclasses that implement concrete types
        """
        raise NotImplementedError("Value.from_model()")

    @staticmethod
    def load_all() -> list[Value]:
        """Loads all artifact models of the given type for the current session."""
        value_models = Value.load_all_models(ArtifactType.VALUE)
        return Value._load_from_models(value_models)

    @staticmethod
    def load_all_with(context: Context, store: ArtifactStore) -> list[Value]:
        """Loads all artifact models of the given type for the given context and store."""
        value_models = Value.load_all_models_with(
            ArtifactType.VALUE, context, store
        )
        return Value._load_from_models(value_models)

    @staticmethod
    def _load_from_models(value_models: list[ArtifactModel]) -> list[Value]:
        """Converts a list of value models (as Artifact Models) into values."""
        values = []
        for artifact_model in value_models:
            value_model: ValueModel = typing.cast(
                ValueModel, artifact_model.body
            )
            value_type: Value = typing.cast(
                Value, load_class(value_model.value_class)
            )
            value = value_type.from_model(artifact_model)
            values.append(value)
        return values

    @classmethod
    def get_class_path(cls) -> str:
        """Returns the full path to this class, including module."""
        return get_class_path(cls)
