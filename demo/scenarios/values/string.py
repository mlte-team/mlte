"""
Implementation of String value.
"""
from __future__ import annotations

from typing import Any

from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.base import ValueBase


class String(ValueBase):
    """An string value."""

    def __init__(self, evidence_metadata: EvidenceMetadata, value: str):
        super().__init__(self, evidence_metadata)

        self.value = value
        """The attribute to store the string in."""

    def serialize(self) -> dict[str, Any]:
        doc: dict[str, Any] = {}
        doc["value"] = self.value
        return doc

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json_: dict[str, Any]
    ) -> String:
        return String(evidence_metadata, json_["value"])

    @classmethod
    def contains(cls, substring: str) -> Condition:
        """Checks if the p-value for multiple ranksums is below given threshold."""
        condition: Condition = Condition(
            "contains",
            [substring],
            lambda value: Success(
                f"Substring '{substring}' is contained in the string value."
            )
            if substring in value.value
            else Failure(
                f"Substring '{substring}' is not contained in the string value."
            ),
        )
        return condition

    @classmethod
    def equal_to(cls, other_string: str) -> Condition:
        """Checks if the p-value for multiple ranksums is below given threshold."""
        condition: Condition = Condition(
            "equal_to",
            [other_string],
            lambda value: Success(
                f"String '{other_string}' is equal to the internal string value."
            )
            if other_string in value.value
            else Failure(
                f"String '{other_string}' is not equal to the internal string value."
            ),
        )
        return condition

    def __str__(self) -> str:
        """Return a string representation of the value."""
        return f"{self.value}"
