"""
mlte/value/types/array.py

Implementation of Array value.
"""

from __future__ import annotations

import typing
from typing import Any, List

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.value.artifact import Value
from mlte.value.model import ArrayValueModel, ValueModel, ValueType


class Array(Value):
    """
    Array implements the Value interface for a numpy array of values.
    """

    def __init__(self, metadata: EvidenceMetadata, array: List[Any]):
        """
        Initialize an Array instance.
        :param metadata: The generating measurement's metadata
        :param array: The numpy array.
        """
        super().__init__(self, metadata)

        self.array: List[Any] = array
        """Underlying values represented as numpy array."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an array value artifact to its corresponding model.
        :return: The artifact model
        """
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ValueModel(
                metadata=self.metadata,
                value_class=self.get_class_path(),
                value=ArrayValueModel(data=self.array),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Array:
        """
        Convert an array value model to its corresponding artifact.
        :param model: The model representation
        :return: The array value
        """
        assert model.header.type == ArtifactType.VALUE, "Broken Precondition."
        body = typing.cast(ValueModel, model.body)

        assert body.value.value_type == ValueType.ARRAY, "Broken Precondition."
        return Array(
            metadata=body.metadata,
            array=body.value.data,
        )

    def __str__(self) -> str:
        return str(self.array)

    def __eq__(self, other: object) -> bool:
        """Comparison between Array values."""
        if not isinstance(other, Array):
            return False
        return self._equal(other)
