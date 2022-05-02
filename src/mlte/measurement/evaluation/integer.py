"""
An EvaluationResult instance for a scalar, integral value.
"""

from .evalution_result import EvaluationResult


class Integer(EvaluationResult):
    """
    Integer implements the EvaluationResult
    interface for a single integer value.
    """

    def __init__(self, measurement, value: int):
        """
        Initialize an Integer instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        :param value: The integer value
        :type value: int
        """
        assert isinstance(value, int), "Argument must be `int`."

        super().__init__(measurement)

        self.value = value
        """The wrapped integer value."""

    def __str__(self) -> str:
        """Return a string representation of the Integer."""
        return f"{self.value}"
