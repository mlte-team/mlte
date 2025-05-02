"""
An Evidence instance for a scalar, integral value.
"""

from __future__ import annotations

import typing
from typing import Callable

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, IntegerValueModel
from mlte.model.base_model import BaseModel
from mlte.validation.validator import Validator


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
        assert isinstance(
            model, ArtifactModel
        ), "Can't create object from non-ArtifactModel model."
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.evidence_type == EvidenceType.INTEGER
        ), "Broken Precondition."
        return Integer(value=body.value.integer).with_metadata(body.metadata)

    def __eq__(self, other: object) -> bool:
        """Comparison between Integer values."""
        if not isinstance(other, Integer):
            return False
        return self._equal(other)

    def __str__(self) -> str:
        """Return a string representation of this Evidence."""
        return f"{self.value}"

    @classmethod
    def less_than(cls, threshold: int) -> Validator:
        """
        Determine if integer is strictly less than `value`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate Evidence.
        """
        bool_exp: Callable[[Integer], bool] = (
            lambda integer: integer.value < threshold
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Integer magnitude is less than threshold {threshold}",
            failure=f"Integer magnitude exceeds threshold {threshold}",
            input_types=[Integer],
        )
        return validator

    @classmethod
    def less_or_equal_to(cls, threshold: int) -> Validator:
        """
        Determine if integer is less than or equal to `value`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate Evidence.
        """
        bool_exp: Callable[[Integer], bool] = (
            lambda integer: integer.value <= threshold
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Integer magnitude is less than or equal to threshold {threshold}",
            failure=f"Integer magnitude exceeds threshold {threshold}",
            input_types=[Integer],
        )
        return validator
