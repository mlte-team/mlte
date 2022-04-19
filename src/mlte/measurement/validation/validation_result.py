"""
The result of measurement validation.
"""

import abc
from typing import List


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


# -----------------------------------------------------------------------------
# Measurement Binding
# -----------------------------------------------------------------------------


class Binding(metaclass=abc.ABCMeta):
    """The base class for measurement bindings."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete ValidationResult."""
        return all(_has_callable(subclass, method) for method in ["__bool__"])

    def __init__(self):
        """
        Initialize a Binding instance.
        """
        raise NotImplementedError("Cannot instantiate abstract Binding")

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise NotImplementedError(
            "Boolean conversion of abstract Binding is ambiguous."
        )


class Bound(Binding):
    """A Bound instance represents a binding from measurement to property."""

    def __init__(self, measurement, *properties: str):
        """
        Initialize a Bound instance.

        :param measurement: The Measurement to which binding is attached
        :type measurement: Measurement
        :param properties: The names of the properties
        to which the measurement is bound
        :type properties: str
        """
        self.measurement_name = measurement.name
        """The name of the measurement that is bound."""
        self.property_names: List[str] = [name for name in properties]
        """The names of the properties to which measurement is bound."""

    def __bool__(str) -> bool:
        """Implicit boolean conversion."""
        return True


class Unbound(Binding):
    """An Unbound instand represents an unbound measurement."""

    def __init__(self):
        """
        Initialize a Unbound instance.
        """
        pass

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return False


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

        self.binding: Binding = Unbound()
        """The Binding for the ValidationResult."""

    def from_validator(self, validator):
        """
        Set the `validator_name` field of the ValidationResult
        to indicate the validator that produced the result.

        :param validator: The Validator instance that produced the result
        :type validator: Validator

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        self.validator_name = validator.name
        return self

    def with_binding(self, binding: Binding):
        """
        Set the `binding` field of the ValidationResult.

        :param binding: The Binding instance
        :type binding: Binding

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        self.binding = binding
        return self


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
