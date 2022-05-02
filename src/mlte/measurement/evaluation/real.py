"""
An EvaluationResult instance for a scalar, real value.
"""

from .evalution_result import EvaluationResult


class Real(EvaluationResult):
    """
    Real implements the EvaluationResult
    interface for a single real value.
    """

    def __init__(self, measurement, value: float):
        """
        Initialize a Real instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        :param value: The real value
        :type value: float
        """
        assert isinstance(value, float), "Argument must be `float`."

        super().__init__(measurement)

        self.value = value
        """The wrapped real value."""

    def __str__(self) -> str:
        """Return a string representation of the Real."""
        return f"{self.value}"
