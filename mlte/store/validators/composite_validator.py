"""Class and interface definitions for top level validators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CompositeValidator:
    """Class to compose CrossValidators."""

    def __init__(self, validators: CrossValidator = []):
        """Initialize a CompositeValidator instance."""

        self.validators: CrossValidator = validators
        """List of validators to execute."""

    def validate_all(self, new_resource: any) -> None:
        """Validate all validators."""
        if self.validators:
            for validator in self.validators:
                validator.validate(new_resource)
        else:
            print("Validators still none, figure out how to make catalog validators work.")


class CrossValidator(ABC):
    """Interface to define a CrossValidator that validates store entries against data in separate stores."""

    # TODO: These are any to avoid circular imports, can this be added somehow?
    def __init__(
        self,
        artifact_store: any = None,
        user_store: any = None,
        custom_list_store: any = None,
    ):
        """
        Initialize a CrossValidator instance.
        :param artifact_store: Artifact store to use for validation.
        :param user_store: Catalog store to use for validation.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.artifact_store = artifact_store
        self.user_store = user_store
        self.custom_list_store = custom_list_store

    @abstractmethod
    def validate(self, new_resource: Any) -> Any:
        """
        Validate a resource.
        :param new_resource: The data to create or edit the resource to be validated
        :return: The validated resource
        :raises RuntimeError: On failed validation
        """
        raise NotImplementedError(
            "Can't validate without a specific implementation."
        )
