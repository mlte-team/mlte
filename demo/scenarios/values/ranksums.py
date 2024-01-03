"""
Implementation of RankSums value.
"""
from __future__ import annotations

from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.types.array import Array


class RankSums(Array):
    """A RankSums array is an array with the results of the ranksums function (stat on first pos, p-value on second)."""

    @classmethod
    def p_value_greater_or_equal_to(cls, threshold: float) -> Condition:
        condition: Condition = Condition(
            "p_value_greater_or_equal_to",
            [threshold],
            lambda value: Success(
                f"P-Value {value.array[1]} is greater or equal to {threshold}"
            )
            if value.array[1] >= threshold
            else Failure(
                f"P-Value {value.array[1]} is less than threshold {threshold}"
            ),
        )
        return condition
