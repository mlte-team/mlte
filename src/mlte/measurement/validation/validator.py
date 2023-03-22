"""
The interface for measurement validation.
"""

import typing
from typing import Callable
from ..result import Result
from ..validation import ValidationResult


class Validator:
    """
    The Validator class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        callback: Callable[[Result], ValidationResult],
    ):
        """
        Initialize a Validator instance.

        :param name: The validator identifier
        :type name: str
        :param callback: The callable that implements validation
        :type callback: Callable[[Result], ValidationResult]
        """
        self.name: str = name
        """The human-readable identifier for the Validator."""

        self.callback: Callable[[Result], ValidationResult] = callback
        """The callback that implements validation."""

    def __call__(self, result: Result) -> ValidationResult:
        """
        Invoke the validation callback

        :param result: The result of measurement evaluation
        :type result: Result

        :return: The result of measurement validation
        :rtype: ValidationResult
        """
        return self.callback(result)._from_validator(self)._with_result(result)
