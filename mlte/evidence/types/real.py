"""
An Evidence instance for a scalar, real value.
"""

from __future__ import annotations

import typing
from typing import Callable, Optional

from mlte.artifact.model import ArtifactModel
from mlte.evidence.artifact import Evidence
from mlte.evidence.model import EvidenceType, RealValueModel
from mlte.measurement.units import (
    Quantity,
    Unit,
    quantity_to_str,
    str_to_unit,
    unit_to_str,
)
from mlte.model.base_model import BaseModel
from mlte.validation.validator import Validator


class Real(Evidence):
    """
    Real implements the Evidence interface for a single real value.
    """

    def __init__(self, value: float, unit: Optional[Unit] = None):
        """
        Initialize a Real instance.
        :param value: The real value
        :param unit: The unit the values comes in, as a value from Units, defaults to None.
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__()

        self.value = value
        """The wrapped real value."""

        self.unit = unit
        """The unit, if any."""

    def get_value_w_units(self) -> Quantity:  # type: ignore[type-arg]
        """
        Returns the float value as a Quantity, potentially with units.
        """
        return Quantity(self.value, self.unit)

    def to_model(self) -> ArtifactModel:
        """
        Convert a real value artifact to its corresponding model.
        :return: The artifact model
        """
        return self._to_artifact_model(
            value_model=RealValueModel(
                real=self.value, unit=unit_to_str(self.unit)
            )
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Real:
        """
        Convert a real value model to its corresponding artifact.
        :param model: The model representation
        :return: The real value
        """
        body = cls._check_proper_types(model, EvidenceType.REAL)
        return Real(
            value=body.value.real,  # type: ignore
            unit=str_to_unit(body.value.unit),  # type: ignore
        ).with_metadata(body.metadata)

    def __str__(self) -> str:
        """Return a string representation of the Real."""
        return f"{self.get_value_w_units() if self.unit else self.value}"

    def __eq__(self, other: object) -> bool:
        """Comparison between Real values."""
        if not isinstance(other, Real):
            return False
        return self._equal(other)

    @classmethod
    def less_than(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Determine if real is strictly less than `threshold`.

        :param threshold: The threshold value
        :param unit: the unit the values comes in, as a value from Units
        :return: The Validator that can be used to validate Evidence.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Real], bool] = (
            lambda real: real.get_value_w_units() < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Real magnitude is less than threshold {quantity_to_str(threshold_w_unit)}",
            failure=f"Real magnitude exceeds threshold {quantity_to_str(threshold_w_unit)}",
            input_types=[Real],
        )
        return validator

    @classmethod
    def less_or_equal_to(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Determine if real is less than or equal to `threshold`.

        :param threshold: The threshold value
        :param unit: the unit the values comes in, as a value from Units
        :return: The Validator that can be used to validate Evidence.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Real], bool] = (
            lambda real: real.get_value_w_units() <= threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Real magnitude is less than or equal to threshold {quantity_to_str(threshold_w_unit)}",
            failure=f"Real magnitude exceeds threshold {quantity_to_str(threshold_w_unit)}",
            input_types=[Real],
        )
        return validator

    @classmethod
    def greater_than(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Determine if real is strictly greater than `threshold`.

        :param threshold: The threshold value
        :param unit: the unit the values comes in, as a value from Units
        :return: The Validator that can be used to validate Evidence.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Real], bool] = (
            lambda real: real.get_value_w_units() > threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Real magnitude is greater than threshold {quantity_to_str(threshold_w_unit)}",
            failure=f"Real magnitude is below threshold {quantity_to_str(threshold_w_unit)}",
            input_types=[Real],
        )
        return validator

    @classmethod
    def greater_or_equal_to(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Determine if real is greater than or equal to `threshold`.

        :param threshold: The threshold value
        :param unit: the unit the values comes in, as a value from Units
        :return: The Validator that can be used to validate Evidence.
        """
        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Real], bool] = (
            lambda real: real.get_value_w_units() >= threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            success=f"Real magnitude is greater than or equal to threshold {quantity_to_str(threshold_w_unit)}",
            failure=f"Real magnitude is below threshold {quantity_to_str(threshold_w_unit)}",
            input_types=[Real],
        )
        return validator

    # Overriden.
    @classmethod
    def load(cls, identifier: typing.Optional[str] = None) -> Real:
        evidence = super().load(identifier)
        return typing.cast(Real, evidence)
