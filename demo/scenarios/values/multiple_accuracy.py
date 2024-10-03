"""
Implementation of MultipleAccuracy value.
"""
from __future__ import annotations

from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.types.array import Array


class MultipleAccuracy(Array):
    """An array with multiple accuracies."""

    @classmethod
    def all_accuracies_more_or_equal_than(cls, threshold: float) -> Condition:
        """Checks if the accuracy for multiple populations is fair by checking if all of them are over the given threshold."""
        condition: Condition = Condition.build_condition(
            lambda value: Success(
                f"All accuracies are equal to or over threshold {threshold}"
            )
            if sum(g >= threshold for g in value.array) == len(value.array)
            else Failure(
                f"One or more accuracies are below threshold {threshold}: {value.array}"
            ),
        )
        return condition
