"""
mlte/value/types/integer.py

A Value instance for a scalar, integral value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.validation import Condition, Failure, Success
from mlte.value.artifact import Value
from mlte.value.model import IntegerValueModel, ValueModel, ValueType


class Integer(Value):
    """
    Integer implements the Value interface for a single integer value.
    """

    def __init__(self, metadata: EvidenceMetadata, value: int):
        """
        Initialize an Integer instance.
        :param identifier: An identifier for the value
        :param value: The integer value
        """
        assert isinstance(value, int), "Argument must be `int`."
        super().__init__(self, metadata)

        self.value = value
        """The wrapped integer value."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an integer value artifact to its corresponding model.
        :return: The artifact model
        """
        print("integer.to_model()")
        a = ArtifactModel(
            header=ArtifactHeaderModel(
                identifier=self.identifier, type=self.type
            ),
            body=ValueModel(
                artifact_type=ArtifactType.VALUE,
                metadata=self.metadata,
                value=IntegerValueModel(
                    value_type=ValueType.INTEGER, integer=self.value
                ),
            ),
        )
        print("return")
        print(a)
        return a

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Integer:  # type: ignore[override]
        """
        Convert an integer value model to its corresponding artifact.
        :param model: The model representation
        :return: The integer value
        """
        assert model.header.type == ArtifactType.VALUE, "Broken Precondition."
        body = typing.cast(ValueModel, model.body)

        assert (
            body.value.value_type == ValueType.INTEGER
        ), "Broken Precondition."
        return Integer(
            metadata=body.metadata,
            value=body.value.integer,
        )

    def __eq__(self, other: object) -> bool:
        """Comparison between Integer values."""
        if not isinstance(other, Integer):
            return False
        return self.value == other.value

    def __neq__(self, other: Integer) -> bool:
        """Comparison between Integer values."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Return a string representation of the Integer."""
        return f"{self.value}"

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
            [value],
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
            [value],
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