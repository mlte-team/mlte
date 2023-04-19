"""
A Value instance for a scalar, integral value.
"""
from __future__ import annotations

from typing import Dict, Any

from ..value import Value
from mlte.validation import Validator, Result, Success, Failure
from mlte.measurement_metadata.measurement_metadata import MeasurementMetadata


class Integer(Value):
    """
    Integer implements the Value interface for a single integer value.
    """

    def __init__(self, measurement_metadata: MeasurementMetadata, value: int):
        """
        Initialize an Integer instance.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement: MeasurementMetadata
        :param value: The integer value
        :type value: int
        """
        assert isinstance(value, int), "Argument must be `int`."

        super().__init__(self, measurement_metadata)

        self.value = value
        """The wrapped integer value."""

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize an Integer to a JSON object.

        :return: The JSON object
        :rtype: Dict[str, Any]
        """
        return {"value": self.value}

    @staticmethod
    def deserialize(
        measurement_metadata: MeasurementMetadata, json: Dict[str, Any]
    ) -> Integer:
        """
        Deserialize an Integer from a JSON object.

        :param measurement_metadata: The generating measurement's metadata
        :type measurement_metadata: MeasurementMetadata
        :param json: The JSON object
        :type json: Dict[str, Any]

        :return: The deserialized instance
        :rtype: Integer
        """
        return Integer(measurement_metadata, json["value"])

    def __str__(self) -> str:
        """Return a string representation of the Integer."""
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between Integer values."""
        if not isinstance(other, Integer):
            return False
        return self.value == other.value

    def __neq__(self, other: Integer) -> bool:
        """Comparison between Integer values."""
        return not self.__eq__(other)

    def less_than(self, value: int) -> Result:
        """
        Determine if integer is strictly less than `value`.

        :param value: The threshold value
        :type value: int

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Validator(
            "less_than",
            lambda integer: Success(
                f"Integer magnitude {integer.value} less than threshold {value}"
            )
            if integer.value < value
            else Failure(
                f"Integer magnitude {integer.value} exceeds threshold {value}"
            ),
        )(self)
        return result

    def less_or_equal_to(self, value: int) -> Result:
        """
        Determine if integer is less than or equal to `value`.

        :param value: The threshold value
        :type value: int

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Validator(
            "less_or_equal_to",
            lambda integer: Success(
                f"Integer magnitude {integer.value} "
                f"less than or equal to threshold {value}"
            )
            if integer.value <= value
            else Failure(
                f"Integer magnitude {integer.value} exceeds threshold {value}"
            ),
        )(self)
        return result
