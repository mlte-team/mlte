#! /usr/bin/env python3


from __future__ import annotations

from typing import Any, Callable, Optional

from mlte.evidence.external import ExternalEvidence
from mlte.measurement.units import Quantity, Unit, str_to_unit, unit_to_str
from mlte.validation.validator import Validator


class CommonStatistics(ExternalEvidence):
    DEFAULT_UNIT: Optional[Unit] = None

    def __init__(
        self, avg: float, min: float, max: float, unit: Optional[Unit]
    ):
        """

        :param avg: The average value
        :param min: The minimum value
        :param max: The maximum value
        :param unit: the unit the values comes in, as a value from Units
        """
        super().__init__()

        self.avg = Quantity(avg, unit)
        """The average value."""

        self.min = Quantity(min, unit)
        """The minimum values."""

        self.max = Quantity(max, unit)
        """The maximum value."""

        self.unit = unit
        """The unit being used for all values."""

    def serialize(self) -> dict[str, Any]:
        """
        Serialize to a JSON object.

        :return: The JSON object
        """
        return {
            "avg": self.avg.magnitude,
            "min": self.min.magnitude,
            "max": self.max.magnitude,
            "unit": unit_to_str(self.unit),
        }

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> Any:
        """
        Deserialize from a JSON object.

        :param data: The JSON object

        :return: The deserialized instance
        """
        unit = str_to_unit(data["unit"])
        return cls(
            avg=data["avg"],
            min=data["min"],
            max=data["max"],
            unit=unit if unit else cls.DEFAULT_UNIT,
        )

    def __str__(self) -> str:
        """Return a string representation."""
        return (
            f"Average: {self.avg}\n"
            + f"Minimum: {self.min}\n"
            + f"Maximum: {self.max}"
        )

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return (
            f"avg={self.avg}, min={self.min}, max={self.max}, unit={self.unit}"
        )

    @classmethod
    def max_utilization_less_than(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Construct and invoke a validator for maximum memory utilization.

        :param threshold: The threshold value for maximum utilization
        :param unit: the unit the threshold comes in, as a value from Units; defaults to DEFAULT_UNIT

        :return: The Validator that can be used to validate a Value.
        """
        # This allows us to get the unit from a subclass
        if unit is None:
            unit = cls.DEFAULT_UNIT

        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Any], bool] = (
            lambda stats: stats.max < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Maximum utilization below threshold {threshold_w_unit}",
            failure=f"Maximum utilization exceeds threshold {threshold_w_unit}",
            input_types=[cls],
        )
        return validator

    @classmethod
    def average_utilization_less_than(
        cls, threshold: float, unit: Optional[Unit] = None
    ) -> Validator:
        """
        Construct and invoke a validator for average memory utilization.

        :param threshold: The threshold value for average utilization, in KB
        :param unit: the unit the threshold comes in, as a value from Units; defaults to Units.kilobyte

        :return: The Validator that can be used to validate a Value.
        """

        # This allows us to get the unit from a subclass
        if unit is None:
            unit = cls.DEFAULT_UNIT

        threshold_w_unit = Quantity(threshold, unit)
        bool_exp: Callable[[Any], bool] = (
            lambda stats: stats.avg < threshold_w_unit
        )
        validator: Validator = Validator.build_validator(
            bool_exp=bool_exp,
            thresholds=[threshold_w_unit],
            success=f"Average utilization below threshold {threshold_w_unit}",
            failure=f"Average utilization exceeds threshold {threshold_w_unit}",
            input_types=[cls],
        )
        return validator
