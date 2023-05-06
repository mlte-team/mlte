"""
Implementation of ConfusionMatrix value.
"""

from __future__ import annotations
from typing import Dict, Any

import numpy as np

from mlte.value import Value
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata
from mlte.validation import (
    Validator,
    Result,
    Success,
    Failure,
)


class ConfusionMatrix(Value):
    def __init__(
        self, measurement_metadata: MeasurementMetadata, matrix: np.ndarray
    ):
        super().__init__(self, measurement_metadata)

        self.matrix: np.ndarray = matrix
        """Underlying matrix represented as numpy array."""

    def serialize(self) -> dict[str, Any]:
        return {"matrix": [[int(val) for val in row] for row in self.matrix]}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json_: dict[str, Any]
    ) -> ConfusionMatrix:
        return ConfusionMatrix(
            measurement_metadata, np.asarray(json_["matrix"])
        )

    def __str__(self) -> str:
        return str(self.matrix)

    def misclassification_count_less_than(self, threshold: int) -> Result:
        return Validator(
            "misclassification_count_less_than",
            lambda cm: Success(
                f"Misclass count {cm.misclassifications} less than threshold {threshold}"
            )
            if cm.misclassifications <= threshold
            else Failure(
                f"Misclassification count {cm.misclassifications} exceeds threshold {threshold}"
            ),
        )(self)

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
