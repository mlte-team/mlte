"""
Implementation of MultipleRaknsums value.
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

from mlte.evidence.external import ExternalEvidence
from mlte.validation.validator import Validator


class MultipleRanksums(ExternalEvidence):
    """An array with multiple ranksums."""

    def __init__(
        self,
        array: np.ndarray,
        num_pops: int = 1,
    ):
        super().__init__()

        self.array = array
        """The array to store data in."""

        self.num_pops: int = num_pops
        """Number of populations or groups.."""

    def serialize(self) -> dict[str, Any]:
        doc: dict[str, Any] = {}
        doc["array"] = [val for val in self.array]
        doc["num_pops"] = self.num_pops
        return doc

    @staticmethod
    def deserialize(json_: dict[str, Any]) -> MultipleRanksums:
        return MultipleRanksums(np.asarray(json_["array"]), json_["num_pops"])

    @classmethod
    def all_p_values_greater_or_equal_than(cls, threshold: float) -> Validator:
        """Checks if the p-value for multiple ranksums is below given threshold."""
        bool_exp: Callable[[MultipleRanksums], bool] = (
            lambda value: len(value.get_low_p_values(threshold)) == 0
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"All p-values are equal to or over threshold {threshold}",
            failure=f"One or more p-values are below threshold {threshold}",
            input_types=[MultipleRanksums],
        )
        return validator

    def get_total_p_value_threshold(self, threshold: float) -> float:
        return threshold / self.num_pops

    def get_low_p_values(self, threshold: float):
        """Generates a dict of all cases that didn't go over the threshold."""
        low_cases = {}

        ranksum: dict[str, list]
        for ranksum in self.array:
            id = next(iter(ranksum))
            pval = ranksum[id][1]
            if pval < self.get_total_p_value_threshold(threshold=threshold):
                low_cases[id] = pval

        return low_cases
