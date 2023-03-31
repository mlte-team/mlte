"""
An EvaluationResult instance for a scalar, real value.
"""

from __future__ import annotations

from typing import Dict, Any

from .result import Result
from ..validation import Validator, ValidationResult, Success, Failure
from ..measurement_metadata import MeasurementMetadata


class Real(Result):
    """
    Real implements the Result
    interface for a single real value.
    """

    def __init__(self, measurement_metadata: MeasurementMetadata, value: float):
        """
        Initialize a Real instance.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement: MeasurementMetadata
        :param value: The real value
        :type value: float
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__(self, measurement_metadata)

        self.value = value
        """The wrapped real value."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an Real to a JSON object.

        :return: The JSON object
        :rtype: Dict[str, Any]
        """
        return {"value": self.value}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> Real:
        """
        Deserialize an Real from a JSON object.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: Real
        """
        return Real(measurement_metadata, json["value"])

    def __str__(self) -> str:
        """Return a string representation of the Real."""
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between Real values."""
        if not isinstance(other, Real):
            return False
        return self.value == other.value

    def __neq__(self, other: Real) -> bool:
        """Comparison between Real values."""
        return not self.__eq__(other)

    def less_than(self, value: float) -> ValidationResult:
        """
        Determine if real is strictly less than `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: ValidationResult
        """
        result: ValidationResult = Validator(
            "less_than",
            lambda real: Success(
                f"Real magnitude {real.value} less than threshold {value}"
            )
            if self.value < value
            else Failure(
                f"Real magnitude {real.value} exceeds threshold {value}"
            ),
        )(self)
        return result

    def less_or_equal_to(self, value: float) -> ValidationResult:
        """
        Determine if real is less than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: ValidationResult
        """
        result: ValidationResult = Validator(
            "less_or_equal_to",
            lambda real: Success(
                f"Real magnitude {real.value} "
                f"less than or equal to threshold {value}"
            )
            if self.value <= value
            else Failure(
                f"Real magnitude {real.value} exceeds threshold {value}"
            ),
        )(self)
        return result

    def greater_than(self, value: float) -> ValidationResult:
        """
        Determine if real is strictly greater than `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: ValidationResult
        """
        result: ValidationResult = Validator(
            "greater_than",
            lambda real: Success(
                f"Real magnitude {real.value} greater than threshold {value}"
            )
            if self.value > value
            else Failure(
                f"Real magnitude {real.value} below threshold {value}"
            ),
        )(self)
        return result

    def greater_or_equal_to(self, value: float) -> ValidationResult:
        """
        Determine if real is greater than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: ValidationResult
        """
        result: ValidationResult = Validator(
            "greater_or_equal_to",
            lambda real: Success(
                f"Real magnitude {real.value} "
                f"greater than or equal to threshold {value}"
            )
            if self.value >= value
            else Failure(
                f"Real magnitude {real.value} below threshold {value}"
            ),
        )(self)
        return result
