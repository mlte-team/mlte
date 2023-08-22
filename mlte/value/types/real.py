"""
mlte/value/types/real.py

An Value instance for a scalar, real value.
"""

from __future__ import annotations

import typing

from mlte.artifact.model import ArtifactHeaderModel, ArtifactModel
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
            header=ArtifactHeaderModel(
                identifier=self.identifier, type=self.type
            ),
            body=ValueModel(
                artifact_type=ArtifactType.VALUE,
                metadata=self.metadata,
                value=RealValueModel(
                    value_type=ValueType.REAL, real=self.value
                ),
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Real:  # type: ignore[override]
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
            [value],
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
            [value],
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
            [value],
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
            [value],
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
