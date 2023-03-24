"""
Defines a condition for a measurement to be approved, including the validator to use and the needed threshold.
"""

from __future__ import annotations

from typing import Any

from mlte.measurement import Measurement
from mlte.measurement.validation import ValidationResult
from mlte.measurement.result import Result
from mlte.measurement.measurement_metadata import MeasurementMetadata
from mlte.measurement.identifier import Identifier

# -----------------------------------------------------------------------------
# Condition
# -----------------------------------------------------------------------------


class Condition:
    def __init__(
        self, measurement: Measurement, validator: str, threshold: Any
    ) -> None:
        """Creates a condition."""
        self.measurement = measurement
        self.validator = validator
        self.threshold = threshold

    def to_json(self) -> dict[str, Any]:
        """Returns this condition as a dictionary."""
        return {
            "name": str(self.measurement.metadata.identifier),
            "type": self.measurement.metadata.typename,
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
        # TODO: make this work. Do we really need to load the measurement type just to create a measurement?
        measurement = Measurement(None, "")
        measurement.metadata = MeasurementMetadata(
            document["type"], Identifier(document["name"])
        )

        return Condition(
            measurement, document["validator"], document["threshold"]
        )

    def validate(self, result: Result) -> ValidationResult:
        """Validates if the given result matches the condition."""
        validator = getattr(result, self.validator)
        validation_result: ValidationResult = validator(self.threshold)
        return validation_result
