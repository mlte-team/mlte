"""
The result of measurement validation.
"""

from __future__ import annotations

import abc
from copy import deepcopy
from typing import Optional

from mlte.value import Value


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


# -----------------------------------------------------------------------------
# Validation Results
# -----------------------------------------------------------------------------


class ValidationResult(metaclass=abc.ABCMeta):
    """The base class for measurement validation results."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete ValidationResult."""
        return all(
            _has_callable(subclass, method)
            for method in ["__bool__", "__str__"]
        )

    def __init__(self):
        """
        Initialize a ValidationResult instance.
        """

        self.validator_name = ""
        """The name of the validator that produced the result."""

        self.value: Optional[Value] = None
        """
        The Value on which the Validator
        that produced this ValidationResult was invoked.
        """

        self.message = ""
        """The message indicating the reason for status."""

    def _with_value(self, value: Value) -> ValidationResult:
        """
        Set the `value` field of the ValidationResult
        to indicate the Value instance from which
        it was generated.

        This hook allows us to embed the value instance within
        the ValidationResult so that we can use the value
        information later when it is used to generate a report.

        :param value: The Value instance on which the
        Validator that produced this instance was invoked
        :type value: Value

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        # TODO(Kyle): This is probably not necessary,
        # and is certainly overkill for the current
        # measurements that we have implemented. Revisit.
        self.value = deepcopy(value)
        return self

    def _from_validator(self, validator) -> ValidationResult:
        """
        Set the `validator_name` field of the ValidationResult
        to indicate the Validator instance from which it was generated.

        This hook allows us to embed the name of the Validator into
        the produced ValidationResult at the point it is produced.

        :param validator: The Validator instance
        :type validator: Validator

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        self.validator_name = validator.name
        return self

    def to_json(self) -> dict[str, str]:
        """
        Returns this object as a JSON dictionary.

        :return: A JSON-like dictionary with this object.
        :rtype: dict[str, str]
        """
        return {
            "name": self.validator_name,
            "result": f"{self}",
            "message": self.message,
        }

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        assert self.value is not None, "Broken precondition."
        if not isinstance(other, ValidationResult):
            return False
        return self.value.identifier == other.value.identifier  # type: ignore

    def __neq__(self, other: object) -> bool:
        """Inequality comparison."""
        return not self.__eq__(other)


class Success(ValidationResult):
    """Indicates successful measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Success validation result instance.

        :param validator_name: The name of the validator
        :type validator_name: str
        :param message: Optional message
        :type message: str
        """
        super().__init__()

        self.message = message
        """The message indicating the reason for success."""

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return True

    def __str__(self) -> str:
        """String representation."""
        return "Success"


class Failure(ValidationResult):
    """Indicates failed measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Failure validation result instance.

        :param validator_name: The name of the validator
        :type validator_name: str
        :param message: Optional message
        :type message: str
        """
        super().__init__()

        self.message = message
        """The message indicating the reason for failure."""

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return False

    def __str__(self) -> str:
        """String representation."""
        return "Failure"


class Ignore(ValidationResult):
    """Indicates ignored measurement validation."""

    def __init__(self, message: str):
        """
        Initialize an Ignore validatation result instance.

        :param message: Message indicating the reason validation is ignored
        :type message: str
        """
        super().__init__()

        self.message = message
        """The message indicating the reason validation is ignored."""

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise RuntimeError("Boolean conversion for Ignore() is ambiguous.")

    def __str__(self) -> str:
        """String representation."""
        return "Ignore"
