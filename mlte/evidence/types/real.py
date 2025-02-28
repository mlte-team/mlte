"""
mlte/value/types/real.py

An Value instance for a scalar, real value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceModel, EvidenceType, RealValueModel
from mlte.model.base_model import BaseModel
from mlte.validation.validator import Validator


class Real(Evidence):
    """
    Real implements the Value interface for a single real value.
    """

    def __init__(self, value: float):
        """
        Initialize a Real instance.
        :param value: The real value
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__()

        self.value = value
        """The wrapped real value."""

    def to_model(self) -> ArtifactModel:
        """
        Convert a real value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=RealValueModel(real=self.value)
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Real:
        """
        Convert a real value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        model = typing.cast(ArtifactModel, model)
        assert (
            model.header.type == ArtifactType.EVIDENCE
        ), "Broken Precondition."
        body = typing.cast(EvidenceModel, model.body)

        assert (
            body.value.value_type == EvidenceType.REAL
        ), "Broken Precondition."
        return Real(value=body.value.real).with_metadata(body.metadata)

    def __str__(self) -> str:
        """Return a string representation of the Real."""
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between Real values."""
        if not isinstance(other, Real):
            return False
        return self._equal(other)

    @classmethod
    def less_than(cls, threshold: float) -> Validator:
        """
        Determine if real is strictly less than `threshold`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate a Value.
        """
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value < threshold,
            success=f"Real magnitude is less than threshold {threshold}",
            failure=f"Real magnitude exceeds threshold {threshold}",
        )
        return validator

    @classmethod
    def less_or_equal_to(cls, threshold: float) -> Validator:
        """
        Determine if real is less than or equal to `threshold`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate a Value.
        """
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value <= threshold,
            success=f"Real magnitude is less than or equal to threshold {threshold}",
            failure=f"Real magnitude exceeds threshold {threshold}",
        )
        return validator

    @classmethod
    def greater_than(cls, threshold: float) -> Validator:
        """
        Determine if real is strictly greater than `threshold`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate a Value.
        """
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value > threshold,
            success=f"Real magnitude is greater than threshold {threshold}",
            failure=f"Real magnitude is below threshold {threshold}",
        )
        return validator

    @classmethod
    def greater_or_equal_to(cls, threshold: float) -> Validator:
        """
        Determine if real is greater than or equal to `threshold`.

        :param threshold: The threshold value
        :return: The Validator that can be used to validate a Value.
        """
        validator: Validator = Validator.build_validator(
            bool_exp=lambda real: real.value >= threshold,
            success=f"Real magnitude is greater than or equal to threshold {threshold}",
            failure=f"Real magnitude is below threshold {threshold}",
        )
        return validator
