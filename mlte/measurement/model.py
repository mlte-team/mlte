"""
Model implementation for the Measurement artifact.
"""

from typing import Any, Optional

from mlte.model.base_model import BaseModel


class MeasurementModel(BaseModel):
    """A description of a validator for a test."""

    measurement_class: str
    """The module/name of the class used for this measurement."""

    measurement_function: Optional[str] = None
    """The module/name of the function used execute the measurement, if external."""

    measurement_args: list[Any] = []
    """The arguments of the function used to execute the measurement."""

    output_class: str
    """The module/class of the output produced by this measurement."""
