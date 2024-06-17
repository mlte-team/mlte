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
        """

        self.spec = spec
        """The specification to be validated."""

        self.values: Dict[str, Value] = {}
        """Where values will be gathered for validation."""

    def add_values(self, values: List[Value]):
        """
        Adds multiple values.

        :param values: The list of values to add to the internal list.
        """
        for value in values:
            self.add_value(value)

    def add_value(self, value: Value):
        """
        Adds a value associated to a property and measurements.

        :param value: The value to add to the internal list.
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
        """
        results = self._validate_results()
        return ValidatedSpec(spec=self.spec, results=results)

    def _validate_results(self) -> Dict[str, Dict[str, Result]]:
        """
        Validates a set of stored Values, and generates Results.

        :return: A dictionary having results for each id, separated by property id.
        """
        # Check that all conditions have values to be validated.
        for conditions in self.spec.properties.values():
            for measurement_id in conditions.keys():
                if measurement_id not in self.values:
                    raise RuntimeError(
                        f"Id '{measurement_id}' does not have a value that can be validated."
                    )

        # Validate and aggregate the results.
        results: Dict[str, Dict[str, Result]] = {}
        for property, conditions in self.spec.properties.items():
            results[property.name] = {}
            for measurement_id, condition in conditions.items():
                results[property.name][measurement_id] = condition(
                    self.values[measurement_id]
                )
        return results
