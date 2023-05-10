"""
A Value instance for a scalar, integral value.
"""
from __future__ import annotations

from typing import Any

from ..value import Value
from mlte.validation import Condition, Success, Failure
from mlte.evidence.evidence_metadata import EvidenceMetadata


class Integer(Value):
    """
    Integer implements the Value interface for a single integer value.
    """

    def __init__(self, evidence_metadata: EvidenceMetadata, value: int):
        """
        Initialize an Integer instance.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param value: The integer value
        :type value: int
        """
        assert isinstance(value, int), "Argument must be `int`."

        super().__init__(self, evidence_metadata)

        self.value = value
        """The wrapped integer value."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize an Integer to a JSON object.

        :return: The JSON object
        :rtype: dict[str, Any]
        """
        return {"value": self.value}

    @staticmethod
    def deserialize(
        evidence_metadata: EvidenceMetadata, json: dict[str, Any]
    ) -> Integer:
        """
        Deserialize an Integer from a JSON object.

        :param evidence_metadata: The generating measurement's metadata
        :type evidence_metadata: EvidenceMetadata
        :param json: The JSON object
        :type json: dict[str, Any]

        :return: The deserialized instance
        :rtype: Integer
        """
        return Integer(evidence_metadata, json["value"])

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

    @classmethod
    def less_than(cls, value: int) -> Condition:
        """
        Determine if integer is strictly less than `value`.

        :param value: The threshold value
        :type value: int

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "less_than",
            lambda integer: Success(
                f"Integer magnitude {integer.value} less than threshold {value}"
            )
            if integer.value < value
            else Failure(
                f"Integer magnitude {integer.value} exceeds threshold {value}"
            ),
        )
        return condition

    @classmethod
    def less_or_equal_to(cls, value: int) -> Condition:
        """
        Determine if integer is less than or equal to `value`.

        :param value: The threshold value
        :type value: int

        :return: The Condition that can be used to validate a Value.
        :rtype: Condition
        """
        condition: Condition = Condition(
            "less_or_equal_to",
            lambda integer: Success(
                f"Integer magnitude {integer.value} "
                f"less than or equal to threshold {value}"
            )
            if integer.value <= value
            else Failure(
                f"Integer magnitude {integer.value} exceeds threshold {value}"
            ),
        )
        return condition
