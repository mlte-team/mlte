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
from mlte._global import global_state, GlobalState
from mlte.store.api import read_spec, write_spec
from mlte.binding import Binding
from .bound_spec import BoundSpec


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


def _check_global_state(state: GlobalState):
    """
    Ensure that the global state contains
    information necessary to save/load results.
    """
    if not state.has_model():
        raise RuntimeError("Set model context prior to saving result.")
    if not state.has_artifact_store_uri():
        raise RuntimeError("Set artifact store URI prior to saving result.")


# -----------------------------------------------------------------------------
# Spec
# -----------------------------------------------------------------------------


class Spec:
    """
    The Spec class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(self, *properties: Property):
        """
        Initialize a Spec instance.

        :param properties: The collection of properties that compose the spec
        :type properties: Property
        """
        # TODO(Kyle): What additional metadata should
        # we store at the level of a Spec?

        self.properties = [p for p in properties]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

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

    # -------------------------------------------------------------------------
    # Save / Load
    # -------------------------------------------------------------------------

    def save(self):
        """Persist the specification to artifact store."""
        state = global_state()
        _check_global_state(state)

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
        _check_global_state(state)

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        document = read_spec(
            artifact_store_uri, model_identifier, model_version
        )
        return Spec._from_json(json=document)

    def _to_json(self) -> Dict[str, Any]:
        """
        Serialize Spec content to JSON document

        :return: The serialized content
        :rtype: Dict[str, Any]
        """
        return {"properties": [p._to_json() for p in self.properties]}

    @staticmethod
    def _from_json(json: Dict[str, Any]) -> Spec:
        """
        Deserialize Spec content from JSON document.

        :param json: The json document
        :type json: Dict[str, Any]

        :return: The deserialized specification
        :rtype: Spec
        """
        return Spec(*[Property._from_json(d) for d in json["properties"]])

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
        self._validate_binding(binding, results, strict)

        properties = [
            self._bind_to_property(property, binding, results)
            for property in self.properties
        ]
        document: Dict[str, Any] = {
            "schema_version": SPEC_LATEST_SCHEMA_VERSION,
            "metadata": self._metadata(),
            "properties": properties,
        }
        return BoundSpec(document)

    def _metadata(self) -> Dict[str, Any]:
        """Generate Spec metadata."""
        state = global_state()
        if not state.has_model():
            raise RuntimeError("Must set model in mlte context.")
        model_identifier, model_version = state.get_model()
        return {
            "model_identifier": model_identifier,
            "model_version": model_version,
            "timestamp": f"{int(time.time())}",
        }

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
    ) -> Dict[str, Any]:
        """
        Collect the results for an individual property
        from result set into a property-level document.

        :param property: The property of interest
        :type property: Property
        :param binding: The mapping from properties to results
        :type binding: Binding
        :param results: The collection of results
        :type results: Iterable[ValidationResult]

        :return: The property-level document
        :rtype: Dict[str, Any]
        """
        # Filter results relevant to property
        targets = set(binding.identifiers_for(property.name))
        assert len(targets) > 0, "Broken invariant."

        results_for_property = [r for r in results if property.name in targets]
        measurements = []
        for _, group in groupby(
            results_for_property, key=lambda vr: vr.result.measurement_typename
        ):
            measurements.append(
                self._bind_for_measurement([vr for vr in group])
            )

        document = {
            "name": property.name,
            "description": property.description,
            "measurements": measurements,
        }
        return document

    def _bind_for_measurement(
        self, results: Iterable[ValidationResult]
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
            result.result.measurement_typename for result in results
        ), "Broken invariant."
        measurement_name = results[0].result.measurement_typename
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

    def __eq__(self, other: Spec) -> bool:
        """Compare Spec instances for equality."""
        return _equal(self, other)

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
    result_identifiers = set(vr.result.identifier.name for vr in results)
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
    result_identifiers = set(vr.result.identifier.name for vr in results)

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
