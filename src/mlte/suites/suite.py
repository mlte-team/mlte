"""
A collection of properties and their measurements.
"""

from __future__ import annotations

import os
import json
from typing import List, Dict, Union

from ..properties import Property
from ..measurement.validation import ValidationResult


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: Iterable

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


JSONValue = Union[str, int, float, List[object], Dict[str, object]]
"""An alias for typed JSON objects."""


class SuiteReport:
    """SuiteReport represents the result of collecting a Suite."""

    def __init__(self, data: Dict[str, JSONValue]):
        """
        Initialize a SuiteReport instance.

        :param data: The data produced by the Suite
        :type data: Dict[str, JSONValue]]
        """
        self.data = data
        """The data produced by the Suite."""


class Suite:
    """
    The Suite class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(self, name: str, *properties: Property):
        """
        Initialize a Suite instance.

        :param properties: The collection of properties that compose the suite
        :type properties: Property
        """
        # TODO(Kyle): What additional metadata should
        # we store at the level of a Suite?

        if not isinstance(name, str):
            raise RuntimeError(f"Invalid name for Suite: {name}")

        self.name = name
        """The human-readable identifier for the Suite."""

        self.properties = [p for p in properties]
        """The collection of properties that compose the Suite."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Suite must be unique.")

    # -------------------------------------------------------------------------
    # Property Manipulation
    # -------------------------------------------------------------------------

    def add_property(self, property: Property):
        """
        Add a property to the suite.

        :param property: The property to add
        :type property: Property
        """
        if property.name in (p.name for p in self.properties):
            raise RuntimeError("Properties in Suite must be unique.")
        self.properties.append(property)

    def has_property(self, name: str) -> bool:
        """
        Determine if the suite contains a particular property.

        :param name: The name of the property
        :type name: str

        :return: `True` if the suite has the property, `False` otherwise
        :rtype: bool
        """
        return any(property.name == name for property in self.properties)

    def get_property(self, name: str) -> Property:
        """
        Get the property with the given identifier, if present.

        :param name: The name of the property
        :type name: str

        :return: The property identified by `name`
        :rtype: Property
        """
        if not self.has_property(name):
            raise RuntimeError(f"Property {name} not found")

        for property in self.properties:
            if property.name == name:
                return property

        raise RuntimeError("Unreachable")

    # -------------------------------------------------------------------------
    # Save / Load
    # -------------------------------------------------------------------------

    def save(self, path: str):
        """
        Save the Suite to `path`.

        :param path: The path to which the Suite is saved
        :type path: str
        """
        # TODO(Kyle): Implement this.
        if path.startswith("s3://"):
            raise NotImplementedError("Save as S3 object not implemented.")

        document = {
            "name": self.name,
            "properties": [
                property._to_document() for property in self.properties
            ],
        }
        with open(path, "w") as f:
            json.dump(document, f)

    @staticmethod
    def from_file(path: str) -> Suite:
        """
        Load a Suite instance from file.

        :param path: The path to the saved Suite
        :type path: str

        :return: The loaded Suite
        :rtype: Suite
        """
        if not os.path.exists(path):
            raise RuntimeError(f"Suite does not exist at path {path}")
        if not os.path.isfile(path):
            raise RuntimeError(f"Suite at path {path} is not a file")

        with open(path, "r") as f:
            document = json.load(f)

        if "name" not in document:
            raise RuntimeError(f"Suite at path {path} missing 'name'")
        if "properties" not in document:
            raise RuntimeError(f"Suite at path {path} missing 'properties'")
        if not isinstance(document["properties"], list):
            raise RuntimeError(f"Suite at path {path} is corrupt")

        suite = Suite(document["name"])
        for pdoc in document["properties"]:
            suite.add_property(Property._from_document(pdoc))

        return suite

    # -------------------------------------------------------------------------
    # Report Generation
    # -------------------------------------------------------------------------

    def collect(self, *results: ValidationResult) -> SuiteReport:
        """
        Collect validation results from all measurements,
        and generate a SuiteReport from these measurements.

        :param results: Validation results
        :type results: ValidationResult

        :return: The suite report
        :rtype: SuiteReport
        """
        pass

    # def collect(self, *results: ValidationResult) -> SuiteResult:
    #     """
    #     Combine validation results from all measurements in the Suite.

    #     :param results: The validation results from all measurements
    #     :type results: ValidationResultSet
    #     """
    #     for property in self.properties:
    #         for measurement in property.measurements:
    #             n_matches = sum(
    #                 1 for r in results if r.token == measurement.token
    #             )
    #             if n_matches == 0:
    #                 raise RuntimeError(
    #                     (
    #                         "No validation result found for property "
    #                         f"{property.name}, measurement {measurement.name}"
    #                     )
    #                 )
    #             elif n_matches > 1:
    #                 raise RuntimeError(
    #                     (
    #                         f"Multiple validation results found for property "
    #                         f"{property.name}, measurement {measurement.name}"
    #                     )
    #                 )

    #     # Format results
    #     output = {}
    #     for property in self.properties:
    #         property_results = {}

    #         for measurement in property.measurements:
    #             measurement_results = {}

    #             validation_results: ValidationResultSet = [
    #                 r for r in results if r.token == measurement.token
    #             ][0]
    #             for validation_result in validation_results:
    #                 measurement_results[validation_result.validator_name] = {
    #                     "result": f"{validation_result}",
    #                     "message": validation_result.message,
    #                 }

    #             property_results[measurement.name] = measurement_results

    #         output[property.name] = property_results

    #     return SuiteResult(output)
