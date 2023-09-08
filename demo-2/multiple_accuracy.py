"""
Implementation of MultipleAccuracy value.
"""
from __future__ import annotations

from array_value import Array

from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success


class MultipleAccuracy(Array):
    """An array with multiple accuracies."""

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
        return sum(g >= threshold for g in self.array) == len(self.array)
