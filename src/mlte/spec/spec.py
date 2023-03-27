"""
A collection of properties and their measurements.
"""

from __future__ import annotations

import time
from itertools import groupby, combinations
from typing import List, Dict, Iterable, Any, Union

from mlte.property import Property
from mlte.measurement.validation import ValidationResult
from mlte._private.schema import SPEC_LATEST_SCHEMA_VERSION
from mlte._global import global_state
from mlte.store.api import read_spec, write_spec
from mlte.binding import Binding
from .bound_spec import BoundSpec
from .condition import Condition
from mlte.measurement.identifier import Identifier
from mlte.measurement.result import Result


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


# -----------------------------------------------------------------------------
# Spec
# -----------------------------------------------------------------------------


class Spec:
    """
    The Spec class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(self, property_conditions: dict[Property, list[Condition]]):
        """
        Initialize a Spec instance.

        :param conditions: The collection of properties that compose the spec, and optionally their conditions.
        :type conditions: dict[Property, list[Condition]]
        """
        # TODO(Kyle): What additional metadata should
        # we store at the level of a Spec?

        self.properties = [p for p in list(property_conditions.keys())]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

        # Store the conditions indexed by property name.
        self.conditions: dict[str, list[Condition]] = {
            property.name: [c for c in conditions]
            for (property, conditions) in property_conditions.items()
        }

        self.results: dict[str, dict[str, Result]] = {}
        """Where temporary results will be gathered for validation."""

    # -------------------------------------------------------------------------
    # Property Manipulation
    # -------------------------------------------------------------------------

    def has_property(self, property: Union[Property, str]) -> bool:
        """
        Determine if the spec contains a particular property.

        :param property: The property itself, or its identifier
        :type property: Union[Property, str]

        :return: `True` if the spec has the property, `False` otherwise
        :rtype: bool
        """
        target_name = property if isinstance(property, str) else property.name
        return any(property.name == target_name for property in self.properties)

    def get_property_for_measurement(self, measurement_id: Identifier):
        """
        Returns the name of a property given a measurement id associated to it.

        :param measurement_id: The identifier of the measurement
        :type measurement_id: Identifier

        :return: The property name if found, None otherwise
        :rtype: str
        """
        for property_name, conditions in self.conditions.items():
            for condition in conditions:
                if condition.measurement_metadata.identifier == measurement_id:
                    return property_name

        return None

    def add_condition(self, property_name: str, condition: Condition):
        """
        Adds the given condition to the property
        """
        if property_name not in self.conditions:
            self.conditions[property_name] = []

        # Check we are not adding a condition again.
        for curr_conditions in self.conditions.values():
            for curr_condition in curr_conditions:
                if curr_condition.get_id() == condition.get_id():
                    raise RuntimeError(
                        f"Condition with id '{condition.get_id()}' alreadty exists for property '{property_name}'"
                    )

        self.conditions[property_name].append(condition)

    # -------------------------------------------------------------------------
    # Save / Load
    # -------------------------------------------------------------------------

    def save(self):
        """Persist the specification to artifact store."""
        state = global_state()
        state.check()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Write spec to store
        write_spec(
            artifact_store_uri, model_identifier, model_version, self._to_json()
        )

    @staticmethod
    def load() -> Spec:
        """
        Load a Spec instance from artifact store.

        :param path: The path to the saved Spec
        :type path: str

        :return: The loaded Spec
        :rtype: Spec
        """
        state = global_state()
        state.check()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        document = read_spec(
            artifact_store_uri, model_identifier, model_version
        )
        return Spec._from_json(json=document)

    # -------------------------------------------------------------------------
    # JSON document generation.
    # -------------------------------------------------------------------------

    def _to_json(self) -> dict[str, Any]:
        """
        Serialize Spec content to JSON-like dict document

        :return: The serialized content
        :rtype: dict[str, Any]
        """
        return self._spec_document(self._properties_document())

    @staticmethod
    def _from_json(json: Dict[str, Any]) -> Spec:
        """
        Deserialize Spec content from JSON document.

        :param json: The json document
        :type json: Dict[str, Any]

        :return: The deserialized specification
        :rtype: Spec
        """
        return Spec(
            {
                Property._from_json(d): [
                    Condition.from_json(c) for c in d["measurements"]
                ]
                for d in json["properties"]
            }
        )

    def _spec_document(
        self, properties_document: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Generate the spec document.

        :return: The spec document
        :rtype: dict[str, Any]
        """
        document = {
            "schema_version": SPEC_LATEST_SCHEMA_VERSION,
            "metadata": self._metadata_document(),
            "properties": properties_document,
        }
        return document

    def _metadata_document(self) -> dict[str, Any]:
        """
        Generate Spec metadata.

        :return: The metadata document
        :rtype: dict[str, Any]
        """
        state = global_state()
        state.check()
        model_identifier, model_version = state.get_model()
        return {
            "model_identifier": model_identifier,
            "model_version": model_version,
            "timestamp": int(time.time()),
        }

    def _properties_document(self) -> list[dict[str, Any]]:
        """
        Generates a document with info an all properties.

        :return: The properties document
        :rtype: dict[str, Any]
        """
        property_docs = [
            self._property_document(
                property,
                [
                    condition.to_json()
                    for condition in self.conditions[property.name]
                ],
            )
            for property in self.properties
        ]
        return property_docs

    def _property_document(
        self, property: Property, measurements: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """
        Generate a property document.

        :param property: The property of interest
        :type property: Property

        :return: The property-level document
        :rtype: dict[str, Any]
        """
        document: dict[str, Any] = property._to_json()
        document["measurements"] = measurements
        return document

    # -------------------------------------------------------------------------
    # Result validation against conditions.
    # -------------------------------------------------------------------------

    def add_result(self, result: Result):
        """Adds a result associated to a property and measurements."""
        measurement_id = result.identifier
        property = self.get_property_for_measurement(measurement_id)
        if property is None:
            raise RuntimeError("Property not found")

        if property not in self.results:
            self.results[property] = {}
        self.results[property][str(measurement_id)] = result

    def validate_and_bind(self) -> BoundSpec:
        """Validates the internal properties given its conditions and the stored results, and generates a BoundSpec from it."""
        validated_results = self._validate_properties()
        return BoundSpec(self._bound_spec_document(validated_results))

    def _validate_properties(self) -> dict[str, list[ValidationResult]]:
        """Validates a set of conditions by property."""
        # Check that all propertoes have results to be validated.
        for property in self.properties:
            if property.name not in self.results:
                raise RuntimeError(
                    f"Property '{property.name}' does not have a result that can be validated."
                )

        results = {
            property.name: self._validate_property(
                property, self.results[property.name]
            )
            for property in self.properties
        }
        return results

    def _validate_property(
        self, property: Property, results: dict[str, Result]
    ) -> list[ValidationResult]:
        """Validates all conditions for a given property, for the given results."""
        conditions = self.conditions[property.name]

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

    # -------------------------------------------------------------------------
    # Specification Binding
    # -------------------------------------------------------------------------

    def bind(
        self,
        binding: Binding,
        results: Iterable[ValidationResult],
        strict: bool = True,
    ) -> BoundSpec:
        """
        Collect validation results and bind them to properties.

        If the `strict` flag is set to `True`, then all properties
        declared in the spec must have at least one (1) result
        bound to them in order to proceed with report generation.
        Spec collection is set to `strict` mode by default.

        :param binding: The binding from properties to result
        :type binding: Binding
        :param results: Validation results
        :type results: ValidationResult
        :param strict: Flag indicating strict measurement requirements
        :type strict: bool

        :return: The bound specification
        :rtype: BoundSpec
        """
        # Validate binding and group validated results by property.
        self._validate_binding(binding, results, strict)
        results_by_property = {
            property.name: self._bind_to_property(property, binding, results)
            for property in self.properties
        }

        return BoundSpec(self._bound_spec_document(results_by_property))

    def _validate_binding(
        self,
        binding: Binding,
        results: Iterable[ValidationResult],
        strict: bool,
    ):
        """
        Validate correctness upon binding.

        :param binding: The binding from properties to result
        :type binding: Binding
        :param results: Collection of ValidationResults
        :type results: ValidationResult
        :param strict: Flag indicating strict measurement requirements
        :type strict: bool

        :raises RuntimeError
        """
        # Ensure that binding and spec are compatible
        _validate_binding_spec_compatibility(binding, self)
        # Ensure that all results are unique
        _validate_result_uniqueness(results)
        # Ensure that each bind point in binding has a result
        _validate_all_bindings_have_result(binding, results)
        if strict:
            # Ensure that every collected result is bound
            _validate_all_results_have_binding(binding, results)

    def _bind_to_property(
        self,
        property: Property,
        binding: Binding,
        results: Iterable[ValidationResult],
    ) -> list[ValidationResult]:
        """
        Collect the results for an individual property
        from result set into a list including only those results.

        :param property: The property of interest
        :type property: Property
        :param binding: The mapping from properties to results
        :type binding: Binding
        :param results: The collection of results
        :type results: Iterable[ValidationResult]

        :return: The property-level document
        :rtype: Dict[str, Any]
        """
        assert all(
            r.result is not None for r in results
        ), "Broken precondition."

        # Filter results relevant to property
        targets = set(binding.identifiers_for(property.name))
        assert len(targets) > 0, "Broken invariant."

        # TODO(Kyle): Clean this up.
        results_for_property = [
            r for r in results if str(r.result.identifier) in targets  # type: ignore
        ]

        return results_for_property

    # -------------------------------------------------------------------------
    # BoundSpec document generation.
    # -------------------------------------------------------------------------

    def _bound_spec_document(
        self, results: dict[str, list[ValidationResult]]
    ) -> dict[str, Any]:
        """Generates a bound spec with the validation results."""
        property_docs = [
            self._validated_property_document(property, results[property.name])
            for property in self.properties
        ]
        return self._spec_document(property_docs)

    def _validated_property_document(
        self, property: Property, results_for_property: list[ValidationResult]
    ) -> Dict[str, Any]:
        """
        Collect results into a property-level document that includes measurement validation results.

        :param result: The validation results to structure
        :type results: list[ValidationResult]

        :return: The measurement-level document
        :rtype: Dict[str, Any]
        """
        measurements = []
        for _, group in groupby(
            results_for_property, key=lambda vr: vr.result.measurement_typename  # type: ignore
        ):
            measurements.append(
                self._measurement_results_document([vr for vr in group])
            )

        document = self._property_document(property, measurements)
        return document

    def _measurement_results_document(
        self, results: List[ValidationResult]
    ) -> Dict[str, Any]:
        """
        Collect results into a measurement-level document.

        :param result: The validation results for the measurement
        :type results: Iterable[ValidationResult]

        :return: The measurement-level document
        :rtype: Dict[str, Any]
        """
        assert len(results) > 0, "Broken invariant."
        assert _all_equal(
            result.result.measurement_typename for result in results  # type: ignore
        ), "Broken invariant."
        measurement_name = results[0].result.measurement_typename  # type: ignore
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

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Compare Spec instances for equality."""
        if not isinstance(other, Spec):
            return False
        reference: Spec = other
        return _equal(self, reference)

    def __neq__(self, other: Spec) -> bool:
        """Compare Spec instances for inequality."""
        return not self.__eq__(other)


def _validate_binding_spec_compatibility(binding: Binding, spec: Spec):
    """
    Validate that a Binding is appropriate for a Spec.

    - Ensure that each property in the spec is included in the binding
    - Ensure that each property in spec has at least 1 associated identifier
    - Ensure that binding does not have extraneous properties

    :param binding: The binding of interest
    :type binding: Binding
    :param spec: The spec of interest
    :type spec: Spec

    :raises: RuntimeError
    """
    for property in spec.properties:
        if len(binding.identifiers_for(property.name)) < 1:
            raise RuntimeError(
                "Binding must include at least"
                f" one mapping for property {property.name}."
            )
    for name in binding.description.keys():
        if not spec.has_property(name):
            raise RuntimeError(
                "Binding contains" f" unnecessary property {name}."
            )


def _validate_result_uniqueness(results: Iterable[ValidationResult]):
    """
    Validate the uniqueness of validation results.

    :param results: The validation results
    :type results: Iterable[ValidationResult]

    :raises RuntimeError: If any two results are equivalent
    """
    for pair in combinations(results, 2):
        # Comparison of ValidationResult compares identifier
        if pair[0] == pair[1]:
            raise RuntimeError("All validation results must be unique")


def _validate_all_bindings_have_result(
    binding: Binding, results: Iterable[ValidationResult]
):
    """
    Ensure that at each identifier in a binding has a corresponding result.

    :param binding: The binding
    :type binding: Binding
    :param results: The collection of results
    :type results: Iterable[ValidationResult]

    :raises: RuntimeError
    """
    result_identifiers = set(vr.result.identifier.name for vr in results)  # type: ignore
    for property_name, identifiers in binding.description.items():
        for identifier in identifiers:
            if identifier not in result_identifiers:
                raise RuntimeError(
                    f"Missing result to bind to {identifier}"
                    f" for property {property_name}."
                )


def _validate_all_results_have_binding(
    binding: Binding, results: Iterable[ValidationResult]
):
    """
    Ensure that each result has a corresponding identifier in binding.

    :param binding: The binding
    :type binding: Binding
    :param results: The collection of results
    :type results: Iterable[ValidationResult]

    :raises: RuntimeError
    """
    result_identifiers = set(vr.result.identifier.name for vr in results)  # type: ignore

    binding_identifiers = set(
        id for collection in binding.description.values() for id in collection
    )
    for result_identifier in result_identifiers:
        if result_identifier not in binding_identifiers:
            raise RuntimeError(
                f"Result with identifier {result_identifier}"
                " is not bound to any property."
            )


def _equal(a: Spec, b: Spec) -> bool:
    """
    Compare Spec instances for equality.

    :param a: Input instance
    :type a: Spec
    :param b: Input instance
    :type b: Spec

    :return: `True` if `a` and `b` are equal, `False` otherwise
    :rtype: bool
    """
    return all(b.has_property(p) for p in a.properties) and all(
        a.has_property(p) for p in b.properties
    )
