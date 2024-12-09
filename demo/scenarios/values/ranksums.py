"""
Implementation of RankSums value.
"""
from __future__ import annotations

from mlte.spec.condition import Condition
from mlte.value.types.array import Array


class RankSums(Array):
    """A RankSums array is an array with the results of the ranksums function (stat on first pos, p-value on second)."""

    @classmethod
    def p_value_greater_or_equal_to(cls, threshold: float) -> Condition:
        condition: Condition = Condition.build_condition(
            bool_exp=lambda value: value.array[1] >= threshold,
            success=f"P-Value is greater or equal to {threshold}",
            failure=f"P-Value is less than threshold {threshold}",
        )
        return condition
