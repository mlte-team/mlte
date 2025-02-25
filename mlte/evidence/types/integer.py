"""
mlte/value/types/integer.py

A Value instance for a scalar, integral value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, IntegerValueModel
from mlte.model.base_model import BaseModel
from mlte.spec.condition import Condition


class Integer(Evidence):
    """
    Integer implements the Value interface for a single integer value.
    """

    def __init__(self, value: int):
        """
        Initialize an Integer instance.
        :param value: The integer value
        """
        assert isinstance(value, int), "Argument must be `int`."
        super().__init__()

        self.value = value
        """The wrapped integer value."""

    def to_model(self) -> ArtifactModel:
        """
        Convert an integer value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=IntegerValueModel(integer=self.value)
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Integer:
        """
        Convert an integer value model to its corresponding artifact.
        :param model: The model representation
        :return: The integer value
        """
        model = typing.cast(ArtifactModel, model)
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.value_type == EvidenceType.INTEGER
        ), "Broken Precondition."
        return typing.cast(
            Integer,
            Integer(
                value=body.value.integer,
            ).with_metadata(body.metadata),
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
    def less_than(cls, threshold: int) -> Condition:
        """
        Determine if integer is strictly less than `value`.

        :param threshold: The threshold value
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            bool_exp=lambda integer: integer.value < threshold,
            success=f"Integer magnitude is less than threshold {threshold}",
            failure=f"Integer magnitude exceeds threshold {threshold}",
        )
        return condition

    @classmethod
    def less_or_equal_to(cls, threshold: int) -> Condition:
        """
        Determine if integer is less than or equal to `value`.

        :param threshold: The threshold value
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            bool_exp=lambda integer: integer.value <= threshold,
            success=f"Integer magnitude is less than or equal to threshold {threshold}",
            failure=f"Integer magnitude exceeds threshold {threshold}",
        )
        return condition
