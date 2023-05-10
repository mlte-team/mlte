"""
Defines a requirement for a measurement to be approved, including the condition to use and the needed threshold.
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
    The Requirement class defines a relation between a measurement,
    a validation method and a threshold/parameter, that will be part of a spec.
    """

    def __init__(
        self,
        identifier: str,
        measurement_type: str,
        condition: str,
        threshold: Any,
    ) -> None:
        """Creates a Requirement."""
        self.identifier = Identifier(identifier)
        self.measurement_type = measurement_type
        self.validator = condition
        self.threshold = threshold

    def to_json(self) -> dict[str, Any]:
        """Returns this requirement as a dictionary."""
        return {
            "identifier": str(self.identifier),
            "measurement_type": self.measurement_type,
            "validator": self.validator,
            "threshold": self.threshold,
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
        if (
            "identifier" not in document
            or "measurement_type" not in document
            or "validator" not in document
            or "threshold" not in document
        ):
            raise RuntimeError("Saved requirement is malformed.")

        return Requirement(
            document["identifier"],
            document["measurement_type"],
            document["validator"],
            document["threshold"],
        )

    def validate(self, value: Value) -> Result:
        """
        Validates if the given value matches the requirement.

        :return: The result of validating this requirement.
        :rtype: Result
        """
        try:
            validator = getattr(value, self.validator)
        except AttributeError:
            raise RuntimeError(
                f"Invalid validation method provided: '{self.validator}()' method not found for value of type {value.typename}"
            )
        condition: Condition = validator(self.threshold)
        result: Result = condition(value)
        return result

    def __str__(self):
        return f"{self.measurement_type}-{self.validator}-{self.threshold}"

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
            and self.measurement_type == reference.measurement_type
            and self.validator == reference.validator
            and self.threshold == reference.threshold
        )

    def __neq__(self, other: Requirement) -> bool:
        """Compare Requirement instances for inequality."""
        return not self.__eq__(other)
