"""
An opaque evaluation evidence, without semantics.
"""

from __future__ import annotations

import typing
from typing import Any, Dict

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, OpaqueValueModel
from mlte.model.base_model import BaseModel


class Opaque(Evidence):
    """
    The 'default' Value instance for measurements that do not provide their own.
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize an Opaque instance.
        :param data: The output of the measurement
        """
        super().__init__()

        self.data = data
        """The raw output from measurement execution."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an opaque value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=OpaqueValueModel(data=self.data)
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Opaque:
        """
        Convert an opaque value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.evidence_type == EvidenceType.OPAQUE
        ), "Broken Precondition."
        return Opaque(data=body.value.data).with_metadata(body.metadata)

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
        return self._equal(other)

    def __str__(self) -> str:
        """Return a string representation of this Evidence."""
        return f"{self.data}"
