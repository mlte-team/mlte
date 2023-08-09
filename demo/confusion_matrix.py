"""
demo/confusion_matrix.py

Implementation of ConfusionMatrix value.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from mlte.evidence.evidence_metadata import EvidenceMetadata
from mlte.validation import Condition, Failure, Result, Success
from mlte.value import Value


class ConfusionMatrix(Value):
    def __init__(self, evidence_metadata: EvidenceMetadata, matrix: np.ndarray):
        super().__init__(self, evidence_metadata)

        self.matrix: np.ndarray = matrix
        """Underlying matrix represented as numpy array."""

    def serialize(self) -> dict[str, Any]:
        return {"matrix": [[int(val) for val in row] for row in self.matrix]}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json_: dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(evidence_metadata, np.asarray(json_["matrix"]))

    def __str__(self) -> str:
        return str(self.matrix)

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
