"""
Implementation of MultipleAccuracy value.
"""

from __future__ import annotations

from mlte.evidence.types.array import Array
from mlte.spec.condition import Condition


class MultipleAccuracy(Array):
    """An array with multiple accuracies."""

    @classmethod
    def all_accuracies_more_or_equal_than(cls, threshold: float) -> Condition:
        """Checks if the accuracy for multiple populations is fair by checking if all of them are over the given threshold."""
        condition: Condition = Condition.build_condition(
            bool_exp=lambda value: sum(g >= threshold for g in value.array)
            == len(value.array),
            success=f"All accuracies are equal to or over threshold {threshold}",
            failure=f"One or more accuracies are below threshold {threshold}",
        )
        return condition
