"""
Implementation of ConfusionMatrix value.
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd

from mlte.evidence.external import ExternalEvidence
from mlte.validation.validator import Validator


class ConfusionMatrix(ExternalEvidence):
    """A sample extension value type."""

    def __init__(self, matrix: np.ndarray):
        super().__init__()

        self.matrix = matrix
        """Underlying matrix represented as two-dimensional array."""

    def serialize(self) -> dict[str, Any]:
        return {"matrix": pd.DataFrame(self.matrix).to_json()}

    @staticmethod
    def deserialize(data: dict[str, Any]) -> ConfusionMatrix:
        return ConfusionMatrix(pd.read_json(data["matrix"]).to_numpy())

    def __str__(self) -> str:
        return f"{self.matrix}".replace("\n", ", ")

    @property
    def misclassifications(self) -> int:
        count: int = 0
        for i in range(len(self.matrix)):
            row = self.matrix[i]
            for j in range(len(row)):
                if i == j:
                    continue
                count += row[j]
        return int(count)

    @classmethod
    def misclassification_count_less_than(cls, threshold: int) -> Validator:
        bool_exp: Callable[[ConfusionMatrix], bool] = (
            lambda cm: cm.misclassifications <= threshold
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Misclass count is less than threshold {threshold}",
            failure=f"Misclassification count exceeds threshold {threshold}",
            input_types=[ConfusionMatrix],
        )
        return validator
