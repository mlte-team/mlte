"""
Defines a condition for a measurement to be approved, including the validator to use and the needed threshold.
"""

from __future__ import annotations

from typing import Any

from mlte.validation import ValidationResult
from mlte.value import Value

# -----------------------------------------------------------------------------
# Condition
# -----------------------------------------------------------------------------


class Condition:
    """
    The Condition class defines a relation between a measurement,
    a validation method and a threshold/parameter, that will be part of a spec.
    """

    def __init__(
        self,
        label: str,
        measurement_type: str,
        validator: str,
        threshold: Any,
    ) -> None:
        """Creates a Condition."""
        self.label = label
        self.measurement_type = measurement_type
        self.validator = validator
        self.threshold = threshold

    def to_json(self) -> dict[str, Any]:
        """Returns this condition as a dictionary."""
        return {
            "label": self.label,
            "measurement_type": self.measurement_type,
            "validator": self.validator,
            "threshold": self.threshold,
        }

    @staticmethod
    def from_json(document: dict[str, Any]) -> Condition:
        """
        Deserialize a Condition from a JSON-like dict document.

        :param json: The json document
        :type json: dict[str, Any]

        :return: The deserialized condition
        :rtype: Condition
        """
        if (
            "label" not in document
            or "measurement_type" not in document
            or "validator" not in document
            or "threshold" not in document
        ):
            raise RuntimeError("Saved condition is malformed.")

        return Condition(
            document["label"],
            document["measurement_type"],
            document["validator"],
            document["threshold"],
        )

    def validate(self, value: Value) -> ValidationResult:
        """
        Validates if the given value matches the condition.

        :return: The result of validating this condition.
        :rtype: ValidationResult
        """
        try:
            validator = getattr(value, self.validator)
        except AttributeError:
            raise RuntimeError(
                f"Invalid validation method provided: '{self.validator}()' method not found for value of type {value.typename}"
            )
        validation_result: ValidationResult = validator(self.threshold)
        return validation_result

    def __str__(self):
        return f"{self.measurement_type}-{self.validator}-{self.threshold}"

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Condition instances for equality."""
        if not isinstance(other, Condition):
            return False
        reference: Condition = other
        return (
            self.label == reference.label
            and self.measurement_type == reference.measurement_type
            and self.validator == reference.validator
            and self.threshold == reference.threshold
        )

    def __neq__(self, other: Condition) -> bool:
        """Compare Condition instances for inequality."""
        return not self.__eq__(other)
