"""
A more detailed collection of properties and their measurements, based on the basic Spec.
"""

from __future__ import annotations

from typing import Any

from mlte.measurement import Identifier
from mlte.measurement.result import Result
from mlte.property import Property
from mlte.spec import Spec
from typing import Any
from .condition import Condition
from mlte.measurement.validation import ValidationResult
from .bound_spec import BoundSpec

# -----------------------------------------------------------------------------
# DetailedSpec
# -----------------------------------------------------------------------------

# TODO: save detailed spec to disk.

class DetailedSpec(Spec):
    """
    The DetailedSpec class integrates properties, measurements,
    validation details, without the actual results for a specific instance.
    """

    def __init__(self, property_conditions: dict[Property, list[Condition]]):
        """
        Initialize a DetailedSpec instance.

        :param conditions: The collection of conditions that compose the spec, separated by property.
        :type conditions: dict[Property, list[Condition]]
        """
        super().__init__(*list(property_conditions.keys()))

        # Store the conditions indexed by property name.
        self.conditions: dict[str, list[Condition]] = {
            property.name: [c for c in conditions]
            for (property, conditions) in property_conditions.items()
        }

        self.results: dict[str, dict[str, Result]] = {}

        # TODO: How to later evaluate the measurements? Semi-automated?

    def get_property(self, measurement_id: Identifier):
        for (property_name, conditions) in self.conditions.items():
            for condition in conditions:
                if condition.measurement.identifier == measurement_id:
                    return property_name
                
        return None
    
    def get_measurement(self, measurement_name: str):
        for (property_name, conditions) in self.conditions.items():
            for condition in conditions:
                if str(condition.measurement.identifier) == measurement_name:
                    return condition.measurement
                
        return None        

    def generate_document(self) -> dict[str, Any]:
        """Generates a document with the detailed spec."""
        property_docs = [
            self._property_document(
                property,
                self._generate_conditions_document(
                    self.conditions[property.name]
                ),
            )
            for property in self.properties
        ]
        document = self._spec_document(property_docs)
        return document

    def _generate_conditions_document(
        self, conditions: list[Condition]
    ) -> list[dict[str, Any]]:
        """Generates a subdocument with the measurements data for a given set of conditions."""
        document = [condition.as_dict() for condition in conditions]
        return document

    ## Evidence

    def add_result(self, result: Result):
        """Adds a result associated to a property and measurements."""
        measurement_id = result.identifier
        property = self.get_property(measurement_id)
        if property is None:
            raise Exception("Property not found")
        if property not in self.results:
            self.results[property]: dict[str, Result] = {}
        self.results[property][str(measurement_id)] = result

    ## Validation.

    def validate_properties(self) -> dict[str, list[ValidationResult]]:
       """Validates a set of conditions by property for the given inputs."""
       results = {property.name: self._validate_property(property, self.results[property.name]) for property in self.properties}
       return results

    def _validate_property(self, property: str, results: dict[str, Result]) -> list[ValidationResult]:
        """Validates all conditions for a given property, for the given inputs."""
        conditions = self.conditions[property.name]
        validation_results = [condition.validate(results[str(condition.measurement.identifier)]) for condition in conditions]
        return validation_results

    def generate_bound_spec(self, results: dict[str, list[ValidationResult]]) -> BoundSpec:
        """Generates a bound spec with the validation results."""
        properties_doc = self._generate_validated_docs(results)
        document = self._spec_document(properties_doc)
        return BoundSpec(document)        

    def _generate_validated_docs(self, results: dict[str, list[ValidationResult]]):
        """Generates a sub document with info, for each property, about its results."""
        property_docs = [
            self._generate_validated_property_doc(
                property,
                results[property.name],
            )
            for property in self.properties
        ]
        return property_docs

    def _generate_validated_property_doc(self, property: Property, results: list[ValidationResult]) -> dict[str, Any]:
        # TODO: add per-measurement grouping, here all will be grouped under the first measurement. (The below method assumes all results are for the same measurement.)
        measurements = [self._bind_for_measurement(results)]
        document = self._property_document(property, measurements)
        return document
