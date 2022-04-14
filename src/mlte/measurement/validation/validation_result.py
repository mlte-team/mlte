"""
The result of measurement validation.
"""

import abc
from typing import List


def _has_callable(type, name) -> bool:
    """Determine if `type` has a callable attribute with the given name."""
    return hasattr(type, name) and callable(getattr(type, name))


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
        raise NotImplementedError(
            "Cannot instantiate abstract ValidationResult."
        )


class ValidationResultSet:
    """A collection of ValidationResult instances."""

    def __init__(self, measurement, results: List[ValidationResult]):
        """
        Initialize a ValidationResultSet instance.

        :param measurement: The generating measurement
        :type measurement: Measurement
        :param results: The collection of ValidationResult
        :type results: Iterable[ValidationResult]
        """
        self.token = measurement.token
        """The token for the originating measurement."""
        self.results = results
        """The collection of validation results."""

    def __len__(self) -> int:
        """
        Return the number of results in the collection.

        :return The number of results in the collection
        :type: int
        """
        return len(self.results)

    def __getitem__(self, index: int) -> ValidationResult:
        """
        Get the validation result at the specified index.

        :param index: The index of interest
        :type index: int

        :return: The validation result
        :rtype: ValidationResult
        """
        return self.results[index]

    def __iter__(self):
        """Iterate over the results of the collection."""
        return (result for result in self.results)


class Success(ValidationResult):
    """Indicates successful measurement validation."""

    def __init__(self, message: str = ""):
        """
        Initialize a Success validation result instance.

        :param message: Optional message
        :type message: str
        """
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

        :param message: Optional message
        :type message: str
        """
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
        self.message = message
        """The message indicating the reason validation is ignored."""

    def __bool__(self) -> bool:
        """Implicit boolean conversion."""
        raise RuntimeError("Boolean conversion for Ignore() is ambiguous.")

    def __str__(self) -> str:
        """String representation."""
        return "Ignore"
