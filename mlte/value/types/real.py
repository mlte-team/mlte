"""
mlte/value/types/real.py

An Value instance for a scalar, real value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success
from mlte.value.artifact import Value
from mlte.value.model import RealValueModel, ValueModel, ValueType


class Real(Value):
    """
    Real implements the Value interface for a single real value.
    """

    def __init__(self, metadata: EvidenceMetadata, value: float):
        """
        Initialize a Real instance.
        :param metadata: The generating measurement's metadata
        :param value: The real value
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__(self, metadata)

        self.value = value
        """The wrapped real value."""

    def to_model(self) -> ArtifactModel:
        """
        Convert a real value artifact to its corresponding model.
        :return: The artifact model
        """
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=ValueModel(
                metadata=self.metadata,
                value_class=self.get_class_path(),
                value=RealValueModel(
                    real=self.value,
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Real:
        """
        Convert a real value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        assert model.header.type == ArtifactType.VALUE, "Broken Precondition."
        body = typing.cast(ValueModel, model.body)

        assert body.value.value_type == ValueType.REAL, "Broken Precondition."
        return Real(
            metadata=body.metadata,
            value=body.value.real,
        )

    def __str__(self) -> str:
        """Return a string representation of the Real."""
        return f"{self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between Real values."""
        if not isinstance(other, Real):
            return False
        return self._equal(other)

    @classmethod
    def less_than(cls, value: float) -> Condition:
        """
        Determine if real is strictly less than `value`.

        :param value: The threshold value
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
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
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
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
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
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
        :return: The Condition that can be used to validate a Value.
        """
        condition: Condition = Condition.build_condition(
            lambda real: Success(
                f"Real magnitude {real.value} "
                f"greater than or equal to threshold {value}"
            )
            if real.value >= value
            else Failure(f"Real magnitude {real.value} below threshold {value}")
        )
        return condition
