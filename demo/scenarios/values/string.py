"""
Implementation of String value.
"""

from __future__ import annotations

from typing import Any

from mlte.evidence.external import ExternalEvidence
from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation.validator import Validator


class String(ExternalEvidence):
    """An string value."""

    def __init__(self, value: str):
        self.value = value
        """The attribute to store the string in."""

    def serialize(self) -> dict[str, Any]:
        doc: dict[str, Any] = {}
        doc["value"] = self.value
        return doc

    @staticmethod
    def deserialize(json_: dict[str, Any]) -> String:
        return String(json_["value"])

    @classmethod
    def contains(cls, substring: str) -> Validator:
        """Checks if the given string is in this one."""
        validator: Validator = Validator.build_validator(
            bool_exp=lambda value: substring in value.value,
            success=f"Substring '{substring}' is contained in the string value.",
            failure=f"Substring '{substring}' is not contained in the string value.",
        )
        return validator

    @classmethod
    def equal_to(cls, other_string: str) -> Validator:
        """Checks if the given string is the same as this one in value."""
        validator: Validator = Validator.build_validator(
            bool_exp=lambda value: other_string == value.value,
            success=f"String '{other_string}' is equal to the internal string value.",
            failure=f"String '{other_string}' is not equal to the internal string value.",
        )
        return validator

    def __str__(self) -> str:
        """Return a string representation of the value."""
        return f"{self.value}"
