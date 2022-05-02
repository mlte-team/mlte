"""
Superclass for all measurements.
"""

from __future__ import annotations

import abc
import typing
from typing import Any, List

from .validation import Binding, Bound, Unbound
from .evaluation import EvaluationResult, Opaque
from .validation import ValidationResult, Validator, Ignore


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

        self.binding: Binding = Unbound()
        """The measurement to property binding."""

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
    def validate(self, *args, **kwargs) -> List[ValidationResult]:
        """
        Evaluate the measurement and validate results.

        :return: The results of measurement validation
        :rtype: List[ValidationResult]
        """
        result = self.evaluate(*args, **kwargs)
        # Invoke each validator on the result of property evaluation;
        # inject the name of the producing validator and the current
        # binding status for the measurement into the ValidationResult
        return [
            validator(result)
            ._from_data(result)
            ._from_validator(validator)
            ._with_binding(self.binding)
            for validator in self.validators
        ]

    def add_validator(self, validator: Validator):
        """
        Add a validator to the measurement.

        :param validator: The validator instance
        :type validator: Validator
        """
        if any(v.name == "__ignore__" for v in self.validators):
            raise RuntimeError("Cannot add validator for ignored measurement.")
        if any(v.name == validator.name for v in self.validators):
            raise RuntimeError("Validator name must be unique.")
        self.validators.append(validator)

    def with_validator(self, validator: Validator) -> Measurement:
        """
        Add a validator to the measurement.

        :param validator: The validator instance
        :type validator: Validator

        :return: The measurement instance (`self`)
        :rtype: Measurement
        """
        self.add_validator(validator)
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

    def _bind(self, *properties: str):
        """
        Bind the Measurement to a particular property.

        :param properties Names of the properties to which measurement is bound
        :type properties: str
        """
        if self._is_bound():
            raise RuntimeError("Cannot bind a bound measurement.")
        self.binding = Bound(self, *properties)

    def _is_bound(self) -> bool:
        """
        Determine if the measurement is already bound.

        :return: `True` if the measurement is bound, `False` otherwise
        :rtype: bool
        """
        return bool(self.binding)
