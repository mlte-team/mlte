"""
Implementation of MultipleAccuracy value.
"""
from __future__ import annotations

from typing import Any

import numpy as np

from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.base import ValueBase


class MultipleAccuracy(ValueBase):
    def __init__(
        self, evidence_metadata: EvidenceMetadata, multiple_accuracy: np.ndarray
    ):
        super().__init__(self, evidence_metadata)

        self.multiple_accuracy: np.ndarray = multiple_accuracy
        """Underlying multiple accuracy represented as numpy array."""

    def serialize(self) -> dict[str, Any]:
        return {"multiple_accuracy": [val for val in self.multiple_accuracy]}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json_: dict[str, Any]
    ) -> MultipleAccuracy:
        return MultipleAccuracy(
            evidence_metadata, np.asarray(json_["multiple_accuracy"])
        )

    def __str__(self) -> str:
        return str(self.multiple_accuracy)

    @classmethod
    def all_accuracies_more_or_equal_than(cls, threshold: float) -> Condition:
        condition: Condition = Condition(
            "all_accuracies_more_than",
            [threshold],
            lambda cm: Success(
                f"All accuracies are equal to or over threshold {threshold}"
            )
            if cm.calculate_all_accuracies_passed(threshold)
            else Failure(
                f"One or more accuracies are below threshold {threshold}"
            ),
        )
        return condition

    def calculate_all_accuracies_passed(self, threshold: float):
        """Calculates if the accuracy for multiple populations is fair by checking if all of them are over the given threshold."""
        return sum(g >= threshold for g in self.multiple_accuracy) == len(
            self.multiple_accuracy
        )
