"""
mlte/spec/requirement.py

Defines a requirement for a measurement to be approved, including the conditions to validate.
"""
from __future__ import annotations

from typing import Any

from mlte.validation import Result, Condition
from mlte.value import Value
from mlte.evidence import Identifier

# -----------------------------------------------------------------------------
# Requirement
# -----------------------------------------------------------------------------


class Requirement:
    """
    The Requirement class defines a named condition that will be used to validate a property.
    """

    def __init__(self, identifier: str, condition: Condition) -> None:
        """Creates a Requirement."""
        self.identifier = Identifier(identifier)
        self.condition = condition

    def to_json(self) -> dict[str, Any]:
        """Returns this requirement as a dictionary."""
        return {
            "identifier": str(self.identifier),
            "condition": self.condition.to_json(),
        }

    @staticmethod
    def from_json(document: dict[str, Any]) -> Requirement:
        """
        Deserialize a Requirement from a JSON-like dict document.

        :param json: The json document
        :type json: dict[str, Any]

        :return: The deserialized requirement
        :rtype: Requirement
        """
        if "identifier" not in document or "condition" not in document:
            raise RuntimeError("Saved requirement is malformed.")

        return Requirement(
            document["identifier"],
            Condition.from_json(document["condition"]),
        )

    def validate(self, value: Value) -> Result:
        """
        Validates if the given value matches the requirement.

        :return: The result of validating this requirement.
        :rtype: Result
        """
        result: Result = self.condition(value)
        return result

    def __str__(self):
        return f"{self.identifier}-{self.condition}"

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Requirement instances for equality."""
        if not isinstance(other, Requirement):
            return False
        reference: Requirement = other
        return (
            self.identifier == reference.identifier
            and self.condition == reference.condition
        )

    def __neq__(self, other: Requirement) -> bool:
        """Compare Requirement instances for inequality."""
        return not self.__eq__(other)
