"""
mlte/value/types/integer.py

A Value instance for a scalar, integral value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.artifact import Value
from mlte.value.model import IntegerValueModel, ValueModel, ValueType


class Integer(Value):
    """
    Integer implements the Value interface for a single integer value.
    """

    def __init__(self, metadata: EvidenceMetadata, value: int):
        """
        Initialize an Integer instance.
        :param metadata: The generating measurement's metadata
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
        a = ArtifactModel(
            header=self.build_artifact_header(),
            body=ValueModel(
                metadata=self.metadata,
                value_class=self.get_class_path(),
                value=IntegerValueModel(
                    integer=self.value,
                ),
            ),
        )
        return a

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Integer:
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
        return self._equal(other)

    def __str__(self) -> str:
        """Return a string representation of the Integer."""
        return f"{self.value}"

    @classmethod
    def less_than(cls, value: int) -> Condition:
        """
        Determine if integer is strictly less than `value`.

        :param value: The threshold value
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            lambda integer: Success(
                f"Integer magnitude {integer.value} less than threshold {value}"
            )
            if integer.value < value
            else Failure(
                f"Integer magnitude {integer.value} exceeds threshold {value}"
            )
        )
        return condition

    @classmethod
    def less_or_equal_to(cls, value: int) -> Condition:
        """
        Determine if integer is less than or equal to `value`.

        :param value: The threshold value
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
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
