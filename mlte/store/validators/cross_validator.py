"""Class and interface definitions for top level validators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CompositeValidator:
    """Class to compose CrossValidators."""

    def __init__(self, validators: list[CrossValidator] = []):
        """Initialize a CompositeValidator instance."""

        self.validators: list[CrossValidator] = validators
        """List of validators to execute."""

    def validate_all(self, new_resource: Any):
        """Validate all validators."""
        if self.validators:
            for validator in self.validators:
                validator.validate(new_resource)


class CrossValidator(ABC):
    """Interface to define a CrossValidator that validates store entries against data in separate stores."""

    @abstractmethod
    def validate(self, new_resource: Any) -> None:
        """
        Validate a resource.
        :param new_resource: The data to create or edit the resource to be validated
        :raises RuntimeError: On failed validation
        """
        raise NotImplementedError(
            "Can't validate without a specific implementation."
        )
