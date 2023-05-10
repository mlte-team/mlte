"""
An Value instance for a scalar, real value.
"""
from __future__ import annotations

from typing import Any

from ..value import Value
from mlte.validation import Condition, Result, Success, Failure
from mlte.evidence.evidence_metadata import EvidenceMetadata


class Real(Value):
    """
    Real implements the Value
    interface for a single real value.
    """

    def __init__(self, evidence_metadata: EvidenceMetadata, value: float):
        """
        Initialize a Real instance.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param value: The real value
        :type value: float
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__(self, evidence_metadata)

        self.value = value
        """The wrapped real value."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an Real to a JSON object.

        :return: The JSON object
        :rtype: dict[str, Any]
        """
        return {"value": self.value}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: dict[str, Any]
    ) -> Real:
        """
        Deserialize an Real from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param json: The JSON object
        :type json: dict[str, Any]

        :return: The deserialized instance
        :rtype: Real
        """
        return Real(evidence_metadata, json["value"])

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

    def less_than(self, value: float) -> Result:
        """
        Determine if real is strictly less than `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Condition(
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

    def less_or_equal_to(self, value: float) -> Result:
        """
        Determine if real is less than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Condition(
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

    def greater_than(self, value: float) -> Result:
        """
        Determine if real is strictly greater than `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Condition(
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

    def greater_or_equal_to(self, value: float) -> Result:
        """
        Determine if real is greater than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The result of validation
        :rtype: Result
        """
        result: Result = Condition(
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
