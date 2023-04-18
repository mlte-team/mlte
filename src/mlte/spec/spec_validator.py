"""
Class in charge of validating a Spec.
"""

from __future__ import annotations

from mlte.property import Property
from mlte.validation import ValidationResult
from .bound_spec import BoundSpec
from mlte.value import Value
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

        self.values: dict[str, dict[str, Value]] = {}
        """Where values will be gathered for validation."""

    def add_value(self, property_name: str, condition_label: str, value: Value):
        """
        Adds a value associated to a property and measurements.

        :param value: The value to add to the list
        :type value: Value
        """
        if property_name not in self.values:
            self.values[property_name] = {}
        self.values[property_name][condition_label] = value

    def validate(self) -> BoundSpec:
        """
        Validates the internal properties given its conditions and the stored values, and generates a BoundSpec from it.

        :return: The validated specification
        :rtype: BoundSpec
        """
        results = self._validate_properties()
        return self.spec.generate_bound_spec(results)

    def _validate_properties(self) -> dict[str, list[ValidationResult]]:
        """
        Validates a set of conditions by property.

        :return: A document indicating, for each property, a list of ValidationResults
        :rtype: dict[str, list[ValidationResult]]
        """
        # Check that all properties have values to be validated.
        for property in self.spec.properties:
            if property.name not in self.values:
                raise RuntimeError(
                    f"Property '{property.name}' does not have a value that can be validated."
                )

        # Validate and aggregate the results for all properties.
        results = {
            property.name: self._validate_property(
                property, self.values[property.name]
            )
            for property in self.spec.properties
        }
        return results

    def _validate_property(
        self, property: Property, values: dict[str, Value]
    ) -> list[ValidationResult]:
        """
        Validates all conditions for a given property, for the given values.

        :param property: The property we want to validate.
        :type property: Property

        :param values: A list of values to validate.
        :type values: dict[str, Value]

        :return: A list of ValidationResults with the validations for all conditions for this property.
        :rtype: list[ValidationResult]
        """
        # Check that all conditions have values to be validated.
        conditions = self.spec.conditions[property.name]
        for condition in conditions:
            if condition.label not in values:
                raise RuntimeError(
                    f"Condition '{condition.label}' does not have a value that can be validated."
                )

        # Validate and aggregate the results for all conditions for this property.
        results = [
            condition.validate(values[condition.label])
            for condition in conditions
        ]
        return results
