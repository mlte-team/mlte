"""
A collection of properties and their measurements.
"""

from __future__ import annotations

from mlte.property import Property
from mlte.measurement.validation import ValidationResult
from .bound_spec import BoundSpec
from mlte.measurement.result import Result
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

        self.results: dict[str, dict[str, Result]] = {}
        """Where temporary results will be gathered for validation."""

    def add_result(self, property_name: str, validator: str, result: Result):
        """
        Adds a result associated to a property and measurements.

        :param result: The result to add to the list
        :type result: Result
        """
        if property_name not in self.results:
            self.results[property_name] = {}
        self.results[property_name][validator] = result

    def validate_and_bind(self) -> BoundSpec:
        """
        Validates the internal properties given its conditions and the stored results, and generates a BoundSpec from it.

        :return: The bound specification
        :rtype: BoundSpec
        """
        validated_results = self._validate_properties()
        return self.spec.generate_bound_spec(validated_results)

    def _validate_properties(self) -> dict[str, list[ValidationResult]]:
        """
        Validates a set of conditions by property.

        :return: A document indicating, for each property, a list of ValidationResults
        :rtype: dict[str, list[ValidationResult]]
        """
        # Check that all propertoes have results to be validated.
        for property in self.spec.properties:
            if property.name not in self.results:
                raise RuntimeError(
                    f"Property '{property.name}' does not have a result that can be validated."
                )

        # Validate and aggregate the results for all properties.
        results = {
            property.name: self._validate_property(
                property, self.results[property.name]
            )
            for property in self.spec.properties
        }
        return results

    def _validate_property(
        self, property: Property, results: dict[str, Result]
    ) -> list[ValidationResult]:
        """
        Validates all conditions for a given property, for the given results.

        :param property: The property we want to validate.
        :type property: Property

        :param results: A list of results to validate, ordered by validator.
        :type results: dict[str, Result]

        :return: A list of ValidationResults with the validations for all conditions for this property.
        :rtype: list[ValidationResult]
        """
        conditions = self.spec.conditions[property.name]

        # Check that all conditions have results to be validated.
        for condition in conditions:
            validator = condition.validator
            if validator not in results:
                raise RuntimeError(
                    f"Condition for validator '{validator}' does not have a result that can be validated."
                )

        # Validate and aggregate the results for all conditions for this property.
        validation_results = [
            condition.validate(results[condition.validator])
            for condition in conditions
        ]
        return validation_results
