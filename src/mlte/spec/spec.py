"""
A collection of properties and their measurements.
"""

from __future__ import annotations

import os
import time
import json
from itertools import groupby, combinations
from typing import List, Dict, Iterable, Any

from ..property import Property
from ..measurement.validation import ValidationResult
from .._private.schema import SPEC_LATEST_SCHEMA_VERSION


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: Iterable

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


def _all_equal(iterable: Iterable[Any]) -> bool:
    """
    Determine if all elements of an iterable are equivalent.

    :param iterable: The iterable
    :type iterable: Iterable[Any]

    :return: `True` if all elements are equal, `False` otherwise
    :rtype: bool
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)  # type: ignore


class SpecReport:
    """SpecReport represents the result of collecting a Spec."""

    def __init__(self, document: Dict[str, Any]):
        """
        Initialize a SpecReport instance.

        :param document: The data produced by the Spec
        :type document: Dict[str, Any]]
        """
        self.document = document
        """The document produced by the Spec."""


class Spec:
    """
    The Spec class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(self, name: str, *properties: Property):
        """
        Initialize a Spec instance.

        :param name: The identifier for the spec
        :type name: str
        :param properties: The collection of properties that compose the spec
        :type properties: Property
        """
        # TODO(Kyle): What additional metadata should
        # we store at the level of a Spec?

        if not isinstance(name, str):
            raise RuntimeError(f"Invalid name for Spec: {name}")

        self.name = name
        """The human-readable identifier for the Spec."""

        self.properties = [p for p in properties]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

    # -------------------------------------------------------------------------
    # Property Manipulation
    # -------------------------------------------------------------------------

    def add_property(self, property: Property):
        """
        Add a property to the spec.

        :param property: The property to add
        :type property: Property
        """
        if property.name in (p.name for p in self.properties):
            raise RuntimeError("Properties in Spec must be unique.")
        self.properties.append(property)

    def has_property(self, name: str) -> bool:
        """
        Determine if the spec contains a particular property.

        :param name: The name of the property
        :type name: str

        :return: `True` if the spec has the property, `False` otherwise
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
        Save the Spec to `path`.

        :param path: The path to which the Spec is saved
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
    def from_file(path: str) -> Spec:
        """
        Load a Spec instance from file.

        :param path: The path to the saved Spec
        :type path: str

        :return: The loaded Spec
        :rtype: Spec
        """
        if not os.path.exists(path):
            raise RuntimeError(f"Spec does not exist at path {path}")
        if not os.path.isfile(path):
            raise RuntimeError(f"Spec at path {path} is not a file")

        with open(path, "r") as f:
            document = json.load(f)

        if "name" not in document:
            raise RuntimeError(f"Spec at path {path} missing 'name'")
        if "properties" not in document:
            raise RuntimeError(f"Spec at path {path} missing 'properties'")
        if not isinstance(document["properties"], list):
            raise RuntimeError(f"Spec at path {path} is corrupt")

        spec = Spec(document["name"])
        for pdoc in document["properties"]:
            spec.add_property(Property._from_document(pdoc))

        return spec

    # -------------------------------------------------------------------------
    # Report Generation
    # -------------------------------------------------------------------------

    def collect(
        self, *results: ValidationResult, strict: bool = True
    ) -> SpecReport:
        """
        Collect validation results from all measurements,
        and generate a spec report from these measurements.

        If the `strict` flag is set to `True`, then all properties
        declared in the spec must have at least one (1) measurement
        bound to them in order to proceed with report generation.
        Spec collection is set to `strict` mode by default.

        :param results: Validation results
        :type results: ValidationResult
        :param strict: Flag indicating strict measurement requirements
        :type strict: bool

        :return: The spec report
        :rtype: SpecReport
        """
        self._validate_uniqueness(*results)
        self._validate_bindings(*results)
        if strict:
            self._validate_property_coverage(*results)

        properties = [
            self._collect_property(property, *results)
            for property in self.properties
        ]
        document: Dict[str, Any] = {
            "schema_version": SPEC_LATEST_SCHEMA_VERSION,
            "name": self.name,
            "timestamp": f"{int(time.time())}",
            "properties": properties,
        }
        return SpecReport(document)

    def _validate_uniqueness(self, *results: ValidationResult):
        """
        Validate the uniqueness of validation results.

        :param results: The validation results
        :type results: ValidationResult

        :raises RuntimeError: If any two results are equivalent
        """
        for pair in combinations(results, 2):
            if pair[0] == pair[1]:
                raise RuntimeError("All validation results must be unique")

    def _validate_bindings(self, *results: ValidationResult):
        """
        Validate bindings.

        :param results: Validation results
        :type results: ValidationResult

        :raises RuntimeError: If any validation result is not bound
        :raises RuntimeError: If any validation result is bound
        to a property that does not exist in the spec
        """
        if not all(r._is_bound() for r in results):
            raise RuntimeError("All ValidationResult must be bound.")
        _ = all(self._validate_bindings_for_result(r) for r in results)

    def _validate_bindings_for_result(self, result: ValidationResult):
        """
        Validate the bindings for an individual ValidationResult.

        :param result: The validation result
        :type result: ValidationResult

        :raises RuntimeError: If any validation result is bound
        to a property that does not exist in the spec
        """
        property_names = [p.name for p in self.properties]
        if not all(
            name in property_names for name in result.binding.property_names
        ):
            raise RuntimeError(
                (
                    f"Result from validator {result.validator_name} "
                    "bound to nonexistent property."
                )
            )

    def _validate_property_coverage(self, *results: ValidationResult):
        """
        Ensure that every property in the spec has at
        least one associated measurement in `results`.

        :param results: The validation results
        :type results: ValidationResult

        :raises RuntimeError: If any property is uncovered
        """
        for property in self.properties:
            if not any(
                property.name in r.binding.property_names for r in results
            ):
                raise RuntimeError(
                    f"Property {property.name} has no bound measurements"
                )

    def _collect_property(
        self, property: Property, *results: ValidationResult
    ) -> Dict[str, Any]:
        """
        Collect the results for an individual property
        from result set into a property-level document.

        :param property: The property of interest
        :type property: Property
        :param results: The result collection
        :type results: ValidationResult

        :return: The property-level document
        :rtype: Dict[str, Any]
        """
        # Filter results relevant to property
        results_for_property = [
            r for r in results if property.name in r.binding.property_names
        ]
        measurements = []
        for _, group in groupby(
            results_for_property, key=lambda vr: vr.binding.measurement_name
        ):
            measurements.append(
                self._collect_measurement(*(vr for vr in group))
            )

        document = {
            "name": property.name,
            "description": property.description,
            "measurements": measurements,
        }
        return document

    def _collect_measurement(
        self, *results: ValidationResult
    ) -> Dict[str, Any]:
        """
        Collect results into a measurement-level document.

        :param result: The validation results for the measurement
        :type results: ValidationResult

        :return: The measurement-level document
        :rtype: Dict[str, Any]
        """
        assert len(results) > 0, "Broken invariant."
        assert _all_equal(
            result.binding.measurement_name for result in results
        ), "Broken invariant."
        measurement_name = results[0].binding.measurement_name
        document = {
            "name": measurement_name,
            "validators": [
                {
                    "name": vr.validator_name,
                    "result": f"{vr}",
                    "message": vr.message,
                }
                for vr in results
            ],
        }
        return document
