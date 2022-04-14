"""
The interface for property validation.
"""

import typing
from typing import Callable
from ..evaluation import EvaluationResult
from ..validation import ValidationResult


class Validator:
    """
    The Validator class defines the interface for property validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        identifier: str,
        callback: Callable[[EvaluationResult], ValidationResult],
    ):
        """
        Initialize a Validator instance.

        :param identifier: The validator identifier
        :type identifier: str
        :param callback: The callable that implements validation
        :type callback: Callable[[EvaluationResult], ValidationResult]
        """
        self.identifier: str = identifier
        """The human-readable identifier for the Validator."""

        self.callback: Callable[[EvaluationResult], ValidationResult] = callback
        """The callback that implements validation."""

    def __call__(self, result: EvaluationResult) -> ValidationResult:
        """
        Invoke the validation callback

        :param result: The result of property evaluation
        :type result: EvaluationResult

        :return: The result of property validation
        :rtype: ValidationResult
        """
        return self.callback(result)
