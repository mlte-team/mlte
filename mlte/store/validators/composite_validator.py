"""Class and interface definitions for top level validators."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

# Needed to avoid circular import issues with store imports in CrossValidator
if TYPE_CHECKING:
    from mlte.store.validators.cross_validator import CrossValidator


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
