"""
Superclass for all model properties.
"""

import abc
import typing
from typing import Any

from .property_token import PropertyToken
from .evaluation import EvaluationResult, Opaque
from .validation import ValidationResultSet, Validator, Ignore


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


class Property(metaclass=abc.ABCMeta):
    """
    The superclass for all model properties.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return all(_has_callable(subclass, method) for method in ["__call__"])

    def __init__(self, name: str):
        """
        Initialize a new Property instance.
        :param name The name of the property
        """
        self.name = name
        """The name of the property (human-readable identifier)"""

        self.token = PropertyToken(self.name)
        """The property token, a unique identifier for the property instance."""

        self.validators = []
        """The collection of property validators."""

    @abc.abstractmethod
    @typing.no_type_check
    def __call__(self, *args, **kwargs) -> Any:
        """Evaluate a property and return results without semantics."""
        raise NotImplementedError("Cannot evaluate abstract property.")

    @typing.no_type_check
    def evaluate(self, *args, **kwargs) -> EvaluationResult:
        """
        Evaluate a property and return results with semantics.

        :return: The result of property execution, with semantics
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
        Evaluate the property and validate results.

        :return: The results of property validation
        :rtype: ValidationResultSet
        """
        result = self.evaluate(*args, **kwargs)
        return ValidationResultSet(
            self, [validator(result) for validator in self.validators]
        )

    def add_validator(self, validator: Validator):
        """
        Add a validator to the property.

        :param validator: The validator instance
        :type validator: Validator
        """
        if any(v.identifier == "__ignore__" for v in self.validators):
            raise RuntimeError("Cannot add validator for ignored property.")
        if any(v.identifier == validator.identifier for v in self.validators):
            raise RuntimeError("Validator identifiers must be unique.")
        self.validators.append(validator)

    def ignore(self, reason: str):
        """
        Indicate that property validation is ignored.

        :param reason: The reason that property validation is ignored
        :type reason: str
        """
        if len(self.validators) > 0:
            raise RuntimeError(
                "Cannot ignore() validation for property with validators."
            )

        self.validators.append(
            Validator("__ignore__", lambda _: Ignore(reason))
        )
