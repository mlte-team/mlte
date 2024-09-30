"""
Implementation of MultipleAccuracy value.
"""
from __future__ import annotations

from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.types.array import Array


class OperationalPerformance(Array):
    """An array with multiple accuracies."""

    @classmethod
    def inference_time_less_than(cls, threshold: float) -> Condition:
        """Checks if the data processing and inference time are less than a fixed time threshold."""
        condition: Condition = Condition(
            "inference_less_than",
            [threshold],
            lambda value: Success(
                f"All accuracies are equal to or over threshold {threshold}"
            )
            if sum(g >= threshold for g in value.array) == len(value.array)
            else Failure(
                f"One or more accuracies are below threshold {threshold}: {value.array}"
            ),
        )
        return condition
