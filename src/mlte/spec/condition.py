"""
Defines a condition for a measurement to be approved, including the validator to use and the needed threshold.
"""

from __future__ import annotations

from typing import Any

from mlte.measurement.validation import ValidationResult
from mlte.measurement.result import Result
from mlte.measurement.measurement_metadata import MeasurementMetadata
from mlte.measurement.identifier import Identifier

# -----------------------------------------------------------------------------
# Condition
# -----------------------------------------------------------------------------


class Condition:
    def __init__(
        self,
        measurement_metadata: MeasurementMetadata,
        validator: str,
        threshold: Any,
    ) -> None:
        """Creates a condition."""
        if type(measurement_metadata) != MeasurementMetadata:
            raise RuntimeError(
                "Object provided to create Condition is not of MeasurementMetadata type."
            )

        self.measurement_metadata = measurement_metadata
        self.validator = validator
        self.threshold = threshold

    def to_json(self) -> dict[str, Any]:
        """Returns this condition as a dictionary."""
        return {
            "name": str(self.measurement_metadata.identifier),
            "type": self.measurement_metadata.typename,
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
            "name" not in document
            or "type" not in document
            or "validator" not in document
            or "threshold" not in document
        ):
            raise RuntimeError("Saved condition is malformed.")

        # Load measurement data.
        measurement_metadata = MeasurementMetadata(
            document["type"], Identifier(document["name"])
        )
        return Condition(
            measurement_metadata, document["validator"], document["threshold"]
        )

    def validate(self, result: Result) -> ValidationResult:
        """Validates if the given result matches the condition."""
        try:
            validator = getattr(result, self.validator)
        except AttributeError:
            raise RuntimeError(
                f"Invalid validation method provided: '{self.validator}()' method not found for result of type {result.typename}"
            )
        validation_result: ValidationResult = validator(self.threshold)
        return validation_result
