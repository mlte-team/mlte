"""
Defines a condition for a measurement to be approved, including the validator to use and the needed threshold.
"""

from __future__ import annotations

from typing import Any

from mlte.measurement import Measurement
from mlte.measurement.validation import ValidationResult
from mlte.measurement.result import Result

# -----------------------------------------------------------------------------
# Condition
# -----------------------------------------------------------------------------


class Condition():

    def __init__(self, measurement: Measurement, validator: str, threshold: Any) -> None:
        self.measurement = measurement
        self.validator = validator
        self.threshold = threshold

    def as_dict(self):
        """Returns this condition as a dictionary."""
        return {
            "name": str(self.measurement.metadata.identifier),
            "type": self.measurement.metadata.typename,
            "validator": self.validator,
            "threshold": self.threshold
        }
    
    def validate(self, result: Result) -> ValidationResult:
        """Validates if the given result matches the condition."""
        validator = getattr(result, self.validator)
        validation_result = validator(self.threshold)
        return validation_result
