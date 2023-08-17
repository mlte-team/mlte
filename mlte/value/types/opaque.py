"""
mlte/value/types/opaque.py

An opaque evaluation value, without semantics.
"""

from __future__ import annotations

import typing
from typing import Any

import deepdiff

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.value.artifact import Value
from mlte.value.model import OpaqueValueModel, ValueModel, ValueType


class Opaque(Value):
    """
    The 'default' Value instance for measurements that do not provide their own.
    """

    def __init__(self, metadata: EvidenceMetadata, data: dict[str, Any]):
        """
        Initialize an Opaque instance.
        :param evidence_metadata: The generating measurement's metadata
        :param data: The output of the measurement
        """
        super().__init__(self, metadata)

        self.data = data
        """The raw output from measurement execution."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an opaque value artifact to its corresponding model.
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
                    value_type=ValueType.OPAQUE, data=self.data
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Opaque:  # type: ignore[override]
        """
        Convert an opaque value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        assert model.header.type == ArtifactType.VALUE, "Broken Precondition."
        body = typing.cast(ValueModel, model.body)

        assert body.value.value_type == ValueType.OPAQUE, "Broken Precondition."
        return Opaque(
            metadata=body.metadata,
            data=body.value.data,
        )

    def __getitem__(self, key: str) -> Any:
        """
        Access an item from the wrapped data object.
        :param key: The key that identifies the item to access
        :raises KeyError: If the key is not present
        :return: The value associated with `key`.
        """
        if key not in self.data:
            raise KeyError(f"Key {key} not found.")
        return self.data[key]

    def __setitem__(self, key: str, value: str) -> None:
        """Raise ValueError to indicate Opaque is read-only."""
        raise ValueError("Opaque is read-only.")

    def __eq__(self, other: object) -> bool:
        """Compare Opaque instances for equality."""
        if not isinstance(other, Opaque):
            return False
        return (
            self.metadata == other.metadata
            and len(deepdiff.DeepDiff(self.data, other.data)) == 0
        )

    def __neq__(self, other: object) -> bool:
        """Compare Opaque instances for inequality."""
        return not self.__eq__(other)
