"""
Implementation of MultipleRaknsums value.
"""
from __future__ import annotations

from typing import Any

import numpy as np
from array_value import Array

from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success


class MultipleRanksums(Array):
    """An array with multiple ranksums."""

    def __init__(
        self,
        evidence_metadata: EvidenceMetadata,
        array: np.ndarray,
        num_pops: int = 1,
    ):
        super().__init__(evidence_metadata, array)

        self.num_pops: int = num_pops
        """Number of populations or groups.."""

    def serialize(self) -> dict[str, Any]:
        doc: dict[str, Any] = super().serialize()
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
        condition: Condition = Condition(
            "all_p_values_greater_or_equal_than",
            [threshold],
            lambda value: Success(
                f"All p-values are equal to or over threshold {threshold}"
            )
            if len(
                [
                    ranksum
                    for ranksum in value.array
                    if ranksum[next(iter(ranksum))][1] < threshold / value.num_pops
                ]
            )
            == 0
            else Failure(
                f"One or more p-values are below threshold {threshold/ value.num_pops}: {value.array}"
            ),
        )
        return condition
