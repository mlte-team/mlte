"""
The result of measurement validation.
"""

from __future__ import annotations

import abc
from copy import deepcopy
from typing import List, Optional

from mlte.measurement.evaluation.evalution_result import EvaluationResult


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
        self.measurement_name = ""
        """The name of the measurement that is bound."""
        self.property_names: List[str] = []
        """The names of the properties to which measurement is bound."""

        raise NotImplementedError("Cannot instantiate abstract Binding")

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise NotImplementedError(
            "Boolean conversion of abstract Binding is ambiguous."
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, Binding):
            raise NotImplementedError(
                f"Equality on Binding and {type(other).__name__}"
            )
        return self.measurement_name == other.measurement_name and set(
            self.property_names
        ) == set(other.property_names)

    def __neq__(self, other: object) -> bool:
        """Inequality comparison."""
        return not (self == other)


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

    def __str__(self) -> str:
        """Return a string representation of Bound."""
        property_names = ",".join(name for name in self.property_names)
        return f"Bound: {self.measurement_name} -> {property_names}"


class Unbound(Binding):
    """An Unbound instand represents an unbound measurement."""

    def __init__(self):
        """
        Initialize a Unbound instance.
        """
        self.measurement_name = ""
        """The name of the measurement that is bound."""
        self.property_names: List[str] = []
        """The names of the properties to which measurement is bound."""

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        return False

    def __str__(self) -> str:
        """Return a string representation of Unbound."""
        return "Unbound"


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

        self.data: Optional[EvaluationResult] = None
        """
        The EvaluationResult on which the Validator
        that produced this ValidationResult was invoked.
        """

        self.binding: Binding = Unbound()
        """The Binding for the ValidationResult."""

        self.message = ""
        """The message indicating the reason for status."""

    def _from_validator(self, validator) -> ValidationResult:
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

    def _from_data(self, data: EvaluationResult) -> ValidationResult:
        """
        Set the `data` field of the ValidationResult
        to indicate the EvaluationResult from which
        it was generated.

        :param data: The EvaluationResult on which the
        Validator that produced this instance was invoked
        :type data: EvaluationResult

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        # TODO(Kyle): This is probably not necessary,
        # and is certainly overkill for the current
        # measurements that we have implemented. Revisit.
        self.data = deepcopy(data)
        return self

    def _with_binding(self, binding: Binding) -> ValidationResult:
        """
        Set the `binding` field of the ValidationResult.

        :param binding: The Binding instance
        :type binding: Binding

        :return: The ValidationResult instance (`self`)
        :rtype: ValidationResult
        """
        self.binding = binding
        return self

    def _is_bound(self) -> bool:
        """
        Determine if the ValidationResult is bound to a property.

        :return: `True` if the result is bound, `False` otherwise
        :rtype: bool
        """
        return bool(self.binding)

    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if not isinstance(other, ValidationResult):
            raise NotImplementedError(
                f"Equality on ValidationResult and {type(other).__name__}"
            )
        return (
            self.validator_name == other.validator_name
            and self.binding == other.binding
        )

    def __neq__(self, other: object) -> bool:
        """Inequality comparison."""
        return not (self == other)


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
