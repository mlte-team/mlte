"""
Implementation of MultipleRaknsums value.
"""

from __future__ import annotations

from typing import Any, Dict

import numpy as np

from mlte.evidence.base import ValueBase
from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition


class MultipleRanksums(ValueBase):
    """An array with multiple ranksums."""

    def __init__(
        self,
        evidence_metadata: EvidenceMetadata,
        array: np.ndarray,
        num_pops: int = 1,
    ):
        super().__init__(evidence_metadata)

        self.array = array
        """The array to store data in."""

        self.num_pops: int = num_pops
        """Number of populations or groups.."""

    def serialize(self) -> Dict[str, Any]:
        doc: dict[str, Any] = {}
        doc["array"] = [val for val in self.array]
        doc["num_pops"] = self.num_pops
        return doc

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json_: dict[str, Any]
    ) -> MultipleRanksums:
        return MultipleRanksums(
            evidence_metadata, np.asarray(json_["array"]), json_["num_pops"]
        )

    @classmethod
    def all_p_values_greater_or_equal_than(cls, threshold: float) -> Condition:
        """Checks if the p-value for multiple ranksums is below given threshold."""
        condition: Condition = Condition.build_condition(
            bool_exp=lambda value: len(value.get_low_p_values(threshold)) == 0,
            success=f"All p-values are equal to or over threshold {threshold}",
            failure=f"One or more p-values are below threshold {threshold}",
        )
        return condition

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
