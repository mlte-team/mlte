"""
Implementation of MultipleAccuracy value.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.value.base import ValueBase
from mlte.value.types.real import Real


class Array(ValueBase):
    def __init__(self, evidence_metadata: EvidenceMetadata, array: np.ndarray):
        super().__init__(self, evidence_metadata)

        self.array: np.ndarray = array
        """Underlying values represented as numpy array."""

    def serialize(self) -> dict[str, Any]:
        return {"array": [val for val in self.array]}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json_: dict[str, Any]
    ) -> Array:
        return Array(evidence_metadata, np.asarray(json_["array"]))

    def __str__(self) -> str:
        return str(self.array)

    def get_as_real(self, position: int, identifier: str = "") -> Real:
        if position >= len(self.array):
            raise RuntimeError(
                f"Position {position} is not in array of size {len(self.array)}"
            )
        return_value = Real(self.metadata, float(self.array[position]))

        # Assign new id if provided.
        if identifier != "":
            return_value.metadata.identifier = Identifier(name=identifier)

        return return_value
