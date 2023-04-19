"""
The interface for measurement validation.
"""

import typing
from typing import Callable
from mlte.value import Value
from ..validation import ValidationResult


class Validator:
    """
    The Validator class defines the interface for measurement validators.
    """

    @typing.no_type_check
    def __init__(
        self,
        name: str,
        callback: Callable[[Value], ValidationResult],
    ):
        """
        Initialize a Validator instance.

        :param name: The validator identifier
        :type name: str
        :param callback: The callable that implements validation
        :type callback: Callable[[Value], ValidationResult]
        """
        self.name: str = name
        """The human-readable identifier for the Validator."""

        self.callback: Callable[[Value], ValidationResult] = callback
        """The callback that implements validation."""

    def __call__(self, value: Value) -> ValidationResult:
        """
        Invoke the validation callback

        :param value: The value of measurement evaluation
        :type value: Value

        :return: The result of measurement validation
        :rtype: ValidationResult
        """
        return (
            self.callback(value)
            ._from_validator(self)
            ._with_measurement_metadata(value.measurement_metadata)
        )
