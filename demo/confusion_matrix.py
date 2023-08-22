"""
demo/confusion_matrix.py

Implementation of ConfusionMatrix value.
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np

from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.base import ValueBase


class ConfusionMatrix(ValueBase):
    """A sample extension value type."""

    def __init__(self, metadata: EvidenceMetadata, matrix: np.ndarray):
        super().__init__(self, metadata)

        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> Dict[str, Any]:
        return {"matrix": self.matrix}

    @staticmethod
    def deserialize(
        metadata: EvidenceMetadata, data: Dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(metadata, data["matrix"])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ConfusionMatrix):
            return False
        return self.matrix == other.matrix

    def __str__(self) -> str:
        return f"{self.matrix}"

    @property
    def misclassifications(self) -> int:
        count = 0
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if i == j:
                    continue
                count += row[j]
        return count

    @classmethod
    def misclassification_count_less_than(cls, threshold: int) -> Condition:
        condition: Condition = Condition(
            "misclassification_count_less_than",
            [threshold],
            lambda cm: Success(
                f"Misclass count {cm.misclassifications} less than threshold {threshold}"
            )
            if cm.misclassifications <= threshold
            else Failure(
                f"Misclassification count {cm.misclassifications} exceeds threshold {threshold}"
            ),
        )
        return condition
