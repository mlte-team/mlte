"""
An Value instance for a scalar, real value.
"""
from __future__ import annotations

from typing import Any

from ..value import Value
from mlte.validation import Condition, Success, Failure
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

    @classmethod
    def less_than(cls, value: float) -> Condition:
        """
        Determine if real is strictly less than `value`.

        :param value: The threshold value
        :type value: float

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "less_than",
            lambda real: Success(
                f"Real magnitude {real.value} less than threshold {value}"
            )
            if real.value < value
            else Failure(
                f"Real magnitude {real.value} exceeds threshold {value}"
            ),
        )
        return condition

    @classmethod
    def less_or_equal_to(cls, value: float) -> Condition:
        """
        Determine if real is less than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "less_or_equal_to",
            lambda real: Success(
                f"Real magnitude {real.value} "
                f"less than or equal to threshold {value}"
            )
            if real.value <= value
            else Failure(
                f"Real magnitude {real.value} exceeds threshold {value}"
            ),
        )
        return condition

    @classmethod
    def greater_than(cls, value: float) -> Condition:
        """
        Determine if real is strictly greater than `value`.

        :param value: The threshold value
        :type value: float

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "greater_than",
            lambda real: Success(
                f"Real magnitude {real.value} greater than threshold {value}"
            )
            if real.value > value
            else Failure(
                f"Real magnitude {real.value} below threshold {value}"
            ),
        )
        return condition

    @classmethod
    def greater_or_equal_to(cls, value: float) -> Condition:
        """
        Determine if real is greater than or equal to `value`.

        :param value: The threshold value
        :type value: float

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "greater_or_equal_to",
            lambda real: Success(
                f"Real magnitude {real.value} "
                f"greater than or equal to threshold {value}"
            )
            if real.value >= value
            else Failure(
                f"Real magnitude {real.value} below threshold {value}"
            ),
        )
        return condition
