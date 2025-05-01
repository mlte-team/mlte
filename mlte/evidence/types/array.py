"""
Implementation of Array Evidence.
"""

from __future__ import annotations

import typing
from typing import Any, List

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import ArrayValueModel, EvidenceModel, EvidenceType
from mlte.model.base_model import BaseModel


class Array(Evidence):
    """
    Array implements the Value interface for a numpy array of values.
    """

    def __init__(self, array: List[Any]):
        """
        Initialize an Array instance.
        :param array: The numpy array.
        """
        super().__init__()

        self.array: List[Any] = array
        """Underlying values represented as numpy array."""

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
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.evidence_type == EvidenceType.ARRAY
        ), "Broken Precondition."
        return Array(array=body.value.data).with_metadata(body.metadata)

    def __str__(self) -> str:
        return str(self.array)

    def __eq__(self, other: object) -> bool:
        """Comparison between Array values."""
        if not isinstance(other, Array):
            return False
        return self._equal(other)
