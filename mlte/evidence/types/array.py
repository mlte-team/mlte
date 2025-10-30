"""
Implementation of Array Evidence.
"""

from __future__ import annotations

import typing
from typing import Any

from mlte.artifact.model import ArtifactModel
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import ArrayValueModel, EvidenceType
from mlte.model.base_model import BaseModel


class Array(Evidence):
    """
    Array implements the Evidence interface for an array of values.
    """

    def __init__(self, array: list[Any]):
        """
        Initialize an Array instance.
        :param array: The array.
        """
        super().__init__()

        self.array: list[Any] = array
        """Underlying values represented as an array."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an array value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=ArrayValueModel(data=self.array)
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Array:
        """
        Convert an array value model to its corresponding artifact.
        :param model: The model representation
        :return: The array value
        """
        body = cls._check_proper_types(model, EvidenceType.ARRAY)
        return Array(array=body.value.data).with_metadata(body.metadata)  # type: ignore

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> Array:
        evidence = super().load(identifier)
        return typing.cast(Array, evidence)

    def __str__(self) -> str:
        return str(self.array)

    def __eq__(self, other: object) -> bool:
        """Comparison between Array values."""
        if not isinstance(other, Array):
            return False
        return self._equal(other)
