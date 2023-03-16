"""
The result of measurement validation.
"""

from __future__ import annotations

import abc
from copy import deepcopy
from typing import Optional

from ..result import Result


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

        self.result: Optional[Result] = None
        """
        The Result on which the Validator
        that produced this ValidationResult was invoked.
        """

        self.message = ""
        """The message indicating the reason for status."""

    def _with_result(self, result: Result) -> ValidationResult:
        """
        Set the `result` field of the ValidationResult
        to indicate the Result instance from which
        it was generated.

        This hook allows us to embed the result instance within
        the ValidationResult so that we can use the result
        information later when it is used to generate a report.

        :param result: The Result instance on which the
        Validator that produced this instance was invoked
        :type result: Result

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        # TODO(Kyle): This is probably not necessary,
        # and is certainly overkill for the current
        # measurements that we have implemented. Revisit.
        self.result = deepcopy(result)
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

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        assert self.result is not None, "Broken precondition."
        if not isinstance(other, ValidationResult):
            return False
        return self.result.identifier == other.result.identifier  # type: ignore

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
