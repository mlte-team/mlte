"""
The result of property validation.
"""

from typing import Iterable


class ValidationResult:
    """The base class for property validation results."""

    def __init__(self, property):
        """
        Initialize a ValidationResult instance.

        :param property: The generating property
        :type property: Property
        """


class ValidationResultSet:
    """A collection of ValidationResult instances."""

    def __init__(self, property, results: Iterable[ValidationResult]):
        """
        Initialize a ValidationResultSet instance.

        :param property: The generating property
        :type property: Property
        :param results: The collection of ValidationResult
        :type results: Iterable[ValidationResult]
        """
        self.token = property.token
        """The token for the originating property."""
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
    """Indicates successful property validation."""

    def __init__(self, message: str = None):
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


class Failure(ValidationResult):
    """Indicates failed property validation."""

    def __init__(self, message: str = None):
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


class Ignore(ValidationResult):
    """Indicates ignored property validation."""

    def __init__(self, message: str):
        """
        Initialize an Ignore validatation result instance.

        :param message: Message indicating the reason validation is ignored
        :type message: str
        """
        self.message = message
        """The message indicating the reason validation is ignored."""
