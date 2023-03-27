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

    def add_result(self, result: Result):
        """
        Adds a result associated to a property and measurements.

        :param result: The result to add to the list
        :type result: Result
        """
        measurement_id = result.identifier
        property = self.spec.get_property_for_measurement(measurement_id)
        if property is None:
            raise RuntimeError("Property not found")

        if property not in self.results:
            self.results[property] = {}
        self.results[property][str(measurement_id)] = result

    def validate_and_bind(self) -> BoundSpec:
        """
        Validates the internal properties given its conditions and the stored results, and generates a BoundSpec from it.

        :return: The bound specification
        :rtype: BoundSpec
        """
        validated_results = self._validate_properties()
        return self.spec.generate_bound_spec(validated_results)

    def _validate_properties(self) -> dict[str, list[ValidationResult]]:
        """Validates a set of conditions by property."""
        # Check that all propertoes have results to be validated.
        for property in self.spec.properties:
            if property.name not in self.results:
                raise RuntimeError(
                    f"Property '{property.name}' does not have a result that can be validated."
                )

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
        """Validates all conditions for a given property, for the given results."""
        conditions = self.spec.conditions[property.name]

        # Check that all conditions have results to be validated.
        for condition in conditions:
            measurement_id = str(condition.measurement_metadata.identifier)
            if measurement_id not in results:
                raise RuntimeError(
                    f"Condition for measurement '{measurement_id}' does not have a result that can be validated."
                )

        # Validate and aggregate the results for all conditions.
        validation_results = [
            condition.validate(
                results[str(condition.measurement_metadata.identifier)]
            )
            for condition in conditions
        ]
        return validation_results
