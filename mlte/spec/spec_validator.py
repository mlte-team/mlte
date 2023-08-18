"""
mlte/spec/spec_validator.py

Class in charge of validating a Spec.
"""

from __future__ import annotations

from typing import Dict

from mlte.validation import Result
from .validated_spec import ValidatedSpec
from mlte.value.artifact import Value
from mlte.spec import Spec


# -----------------------------------------------------------------------------
# SpecValidator
# -----------------------------------------------------------------------------


class SpecValidator:
    """
    Helper class to validate a spec.
    """

    def __init__(self, spec: Spec):
        """
        Initialize a SpecValidator instance.

        :param spec: The specification to be validated
        :type spec: Spec
        """

        self.spec = spec
        """The specification to be validated."""

        self.values: Dict[str, Value] = {}
        """Where values will be gathered for validation."""

    def add_value(self, value: Value):
        """
        Adds a value associated to a property and measurements.

        :param value: The value to add to the list
        :type value: Value
        """
        if value.metadata.get_id() in self.values:
            raise RuntimeError(
                f"Can't have two values with the same id: {value.metadata.get_id()}"
            )
        self.values[value.metadata.get_id()] = value

    def validate(self) -> ValidatedSpec:
        """
        Validates the internal properties given its requirements and the stored values, and generates a ValidatedSpec from it.

        :return: The validated specification
        :rtype: ValidatedSpec
        """
        results = self._validate_results()
        return ValidatedSpec(self.spec, results)

    def _validate_results(self) -> Dict[str, Result]:
        """
        Validates a set of stored results.

        :return: A document indicating the Result for each identifier.
        :rtype: Dict[str, Result]
        """
        # Check that all requirements have values to be validated.
        for _, requirement_list in self.spec.requirements.items():
            for requirement in requirement_list:
                if str(requirement.identifier) not in self.values:
                    raise RuntimeError(
                        f"Requirement '{requirement.identifier}' does not have a value that can be validated."
                    )

        # Validate and aggregate the results.
        results = {}
        for _, requirement_list in self.spec.requirements.items():
            for requirement in requirement_list:
                results[str(requirement.identifier)] = requirement.validate(
                    self.values[str(requirement.identifier)]
                )
        return results
