"""
The interface for measurement validation.
"""

import typing
from typing import Callable
from ..evaluation import EvaluationResult
from ..validation import ValidationResult


class Validator:
    """
    The Validator class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        callback: Callable[[EvaluationResult], ValidationResult],
    ):
        """
        Initialize a Validator instance.

        :param name: The validator identifier
        :type name: str
        :param callback: The callable that implements validation
        :type callback: Callable[[EvaluationResult], ValidationResult]
        """
        self.name: str = name
        """The human-readable identifier for the Validator."""

        self.callback: Callable[[EvaluationResult], ValidationResult] = callback
        """The callback that implements validation."""

    def __call__(self, result: EvaluationResult) -> ValidationResult:
        """
        Invoke the validation callback

        :param result: The result of measurement evaluation
        :type result: EvaluationResult

        :return: The result of measurement validation
        :rtype: ValidationResult
        """
        return self.callback(result)
