"""
mlte/spec/spec_validator.py

Class in charge of validating a Spec.
"""

from __future__ import annotations

from typing import Dict, List

from mlte.spec.spec import Spec
from mlte.validation.result import Result
from mlte.validation.validated_spec import ValidatedSpec
from mlte.value.artifact import Value

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

    def add_values(self, values: List[Value]):
        """Adds multiple values."""
        for value in values:
            self.add_value(value)

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
        # Check that all conditions have values to be validated.
        for conditions in self.spec.properties.values():
            for measurement_id in conditions.keys():
                if measurement_id not in self.values:
                    raise RuntimeError(
                        f"Id '{measurement_id}' does not have a value that can be validated."
                    )

        # Validate and aggregate the results.
        results = {}
        for conditions in self.spec.properties.values():
            for measurement_id, condition in conditions.items():
                results[measurement_id] = condition(self.values[measurement_id])
        return results
