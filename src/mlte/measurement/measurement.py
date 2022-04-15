"""
Superclass for all measurements.
"""

import abc
import typing
from typing import Any, List

from .measurement_token import MeasurementToken
from .evaluation import EvaluationResult, Opaque
from .validation import ValidationResultSet, Validator, Ignore


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Measurement(metaclass=abc.ABCMeta):
    """
    The superclass for all model measurements.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete measurements."""
        return all(_has_callable(subclass, method) for method in ["__call__"])

    def __init__(self, name: str):
        """
        Initialize a new Measurement instance.
        :param name The name of the measurement
        """
        self.name = name
        """The name of the measurement (human-readable identifier)"""

        self.token = MeasurementToken(self.name)
        """A unique identifier for the measurement instance."""

        self.validators: List[Validator] = []
        """The collection of measurement validators."""

    @abc.abstractmethod
    @typing.no_type_check
    def __call__(self, *args, **kwargs) -> Any:
        """Evaluate a measurement and return results without semantics."""
        raise NotImplementedError("Cannot evaluate abstract measurement.")

    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> EvaluationResult:
        """
        Evaluate a measurement and return results with semantics.

        :return: The result of measurement execution, with semantics
        :rtype: EvaluationResult
        """
        data = self(*args, **kwargs)
        return (
            self.semantics(data)
            if hasattr(self, "semantics")
            else Opaque(self, data)
        )

    @typing.no_type_check
    def validate(self, *args, **kwargs) -> ValidationResultSet:
        """
        Evaluate the measurement and validate results.

        :return: The results of measurement validation
        :rtype: ValidationResultSet
        """
        result = self.evaluate(*args, **kwargs)
        return ValidationResultSet(
            self,
            [
                validator(result).from_validator(validator.identifier)
                for validator in self.validators
            ],
        )

    def with_validator(self, validator: Validator) -> Measurement:
        """
        Add a validator to the measurement.

        :param validator: The validator instance
        :type validator: Validator

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        if any(v.identifier == "__ignore__" for v in self.validators):
            raise RuntimeError("Cannot add validator for ignored measurement.")
        if any(v.identifier == validator.identifier for v in self.validators):
            raise RuntimeError("Validator identifiers must be unique.")
        self.validators.append(validator)
        return self

    def ignore(self, reason: str):
        """
        Indicate that measurement validation is ignored.

        :param reason: The reason that measurement validation is ignored
        :type reason: str

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        if len(self.validators) > 0:
            raise RuntimeError(
                "Cannot ignore() validation for measurement with validators."
            )

        self.validators.append(
            Validator("__ignore__", lambda _: Ignore(reason))
        )
        return self
