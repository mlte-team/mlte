"""
An EvaluationResult instance for single, integer values.
"""

from .evalution_result import EvaluationResult


class Integer(EvaluationResult):
    """
    Integer implements the EvaluationResult
    interface for a single integer value.
    """

    def __init__(self, property, value: int):
        """
        Initialize an Integer instance.

        :param property: The generating property
        :type property: Property
        :param value: The integer value
        :type value: int
        """
        super().__init__(property)
        self.value = value

    def __str__(self) -> str:
        """Return a string representation of the Integer."""
        return f"{self.value}"
