"""
A collection of properties and their measurements.
"""

from typing import List, Dict, Any

from ..properties import Property
from ..measurement.validation import ValidationResultSet


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: Iterable

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


class SuiteResult:
    """SuiteResult represents the result of collecting a Suite."""

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a SuiteResult instance.

        :param data: The data produced by the Suite
        :type data: Dict[str, Any]
        """
        self.data = data
        """The data produced by the Suite."""


class Suite:
    """
    The Suite class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(self, *properties: Property):
        """
        Initialize a Suite instance.

        :param properties: The collection of properties that compose the suite
        :type properties: Property
        """
        self.properties = [p for p in properties]
        """The collection of properties that compose the Suite."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Suite must be unique.")

    def add_property(self, property: Property):
        """
        Add a property to the suite.

        :param property: The property to add
        :type property: Property
        """
        if property.name in (p.name for p in self.properties):
            raise RuntimeError("Properties in Suite must be unique.")
        self.properties.append(property)

    def collect(self, *results: ValidationResultSet) -> SuiteResult:
        """
        Combine validation results from all measurements in the Suite.

        :param results: The validation results from all measurements
        :type results: ValidationResultSet
        """
        for property in self.properties:
            for measurement in property.measurements:
                n_matches = sum(
                    1 for r in results if r.token == measurement.token
                )
                if n_matches == 0:
                    raise RuntimeError(
                        (
                            "No validation result found for property "
                            f"{property.name}, measurement {measurement.name}"
                        )
                    )
                elif n_matches > 1:
                    raise RuntimeError(
                        (
                            f"Multiple validation results found for property "
                            f"{property.name}, measurement {measurement.name}"
                        )
                    )

        # Format results
        output = {}
        for property in self.properties:
            property_results = {}

            for measurement in property.measurements:
                measurement_results = {}

                validation_results: ValidationResultSet = [
                    r for r in results if r.token == measurement.token
                ][0]
                for validation_result in validation_results:
                    measurement_results[validation_result.validator_name] = {
                        "result": f"{validation_result}",
                        "message": validation_result.message,
                    }

                property_results[measurement.name] = measurement_results

            output[property.name] = property_results

        return SuiteResult(output)
