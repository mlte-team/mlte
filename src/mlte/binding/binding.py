"""
Implementation of Binding and related types.
"""

from __future__ import annotations

from itertools import combinations
from typing import Dict, List, Any, Iterable

from mlte.property import Property
from mlte.measurement.validation import ValidationResult
from mlte.spec import Spec
from mlte.spec.bound_spec import BoundSpec
from mlte._global import global_state
from mlte.store.api import read_binding, write_binding
from mlte._private.schema import BINDING_LATEST_SCHEMA_VERSION


def _verify_integrity(description: Dict[str, List[str]]):
    """
    Verify the integrity of a Binding description.

    :param description: The description
    :type description: Dict[str, List[str]]
    """
    # Ensure that all keys are `str`
    for k in description.keys():
        if not isinstance(k, str):
            raise RuntimeError("All property identifiers must be `str`.")
    # Ensure all values are `list`
    for v in description.values():
        if not isinstance(v, list):
            raise RuntimeError("All values in Binding must be `list`.")
    # Ensure all values in each list are `str`
    for v in description.values():
        for e in v:
            if not isinstance(e, str):
                raise RuntimeError("All result identifiers must be `str`.")


class Binding:
    """
    A binding represents a mapping from properties
    to the result identifiers with which they are associated.
    """

    def __init__(self, description: Dict[str, List[str]]):
        """
        Initialize a new Binding instance.

        :param description: Description that maps properties to measurements
        :type description: Dict[str, List[str]]
        """
        _verify_integrity(description)
        self.description = description

    def identifiers_for(self, property_name: str) -> List[str]:
        """
        Return the identifiers corresponding to a particular property name.

        :param property_name: The name of the property\
        :type property_name: str
        :return: A collection of result identifiers
        :rtype: List[str]
        """
        # TODO(Kyle): Should this actually not throw on key error?
        return (
            self.description[property_name]
            if property_name in self.description
            else []
        )

    def save(self):
        """Save the Binding instance to artifact store."""
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Write the binding to the artifact store
        write_binding(
            artifact_store_uri,
            model_identifier,
            model_version,
            self._serialize(),
        )

    @staticmethod
    def load() -> Binding:
        """
        Load a binding from the artifact store.

        :return: The saved binding
        :rtype: Binding
        """
        state = global_state()
        state.ensure_initialized()

        model_identifier, model_version = state.get_model()
        artifact_store_uri = state.get_artifact_store_uri()

        # Read the binding from the artifact store
        data = read_binding(artifact_store_uri, model_identifier, model_version)
        return Binding(description=Binding._deserialize(data))

    def _serialize(self) -> Dict[str, Any]:
        """
        Serialize internal data to JSON document.

        :return: The serialized representation of the Binding instance
        :rtype: Dict[str, Any]
        """
        return {
            "schema_version": BINDING_LATEST_SCHEMA_VERSION,
            "properties": [
                self._serialize_property(property_name)
                for property_name in self.description.keys()
            ],
        }

    def _serialize_property(self, property_name: str) -> Dict[str, Any]:
        """
        Serialize an individual property within the binding.

        :param property_name: The name of the property to serialize
        :type property_name: str

        :return: The serialized content
        :rtype: Dict[str, Any]
        """
        assert property_name in self.description, "Broken precondition."
        return {
            "name": property_name,
            "results": [
                self._serialize_result(result_id)
                for result_id in self.description[property_name]
            ],
        }

    def _serialize_result(self, result_id: str) -> Dict[str, Any]:
        """
        Serialize an individual result within the binding.

        :param result_id: The result identifier
        :type result_id: str

        :return: The serialized content
        :rtype: Dict[str, Any]
        """
        return {"identifier": result_id}

    @staticmethod
    def _deserialize(document: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Deserialize binding from JSON document.

        :param document: The JSON document
        :type document: Dict[str, Any]

        :return: The deserialized descritption
        :rtype: Dict[str, List[str]]
        """
        description = {}
        for property in document["properties"]:
            description[property["name"]] = [
                result["identifier"] for result in property["results"]
            ]
        return description

    # -------------------------------------------------------------------------
    # Specification Binding
    # -------------------------------------------------------------------------

    def bind(
        self,
        spec: Spec,
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
        self._validate_binding(results, strict, spec)

        results_by_property = {
            property.name: self._bind_to_property(property, results)
            for property in spec.properties
        }

        return spec.generate_bound_spec(results_by_property)

    def _validate_binding(
        self,
        results: Iterable[ValidationResult],
        strict: bool,
        spec: Spec,
    ):
        """
        Validate correctness upon binding.

        :param results: Collection of ValidationResults
        :type results: ValidationResult
        :param strict: Flag indicating strict measurement requirements
        :type strict: bool

        :raises RuntimeError
        """
        self._validate_binding_spec_compatibility(spec)

        # Ensure that all results are unique
        _validate_result_uniqueness(results)
        # Ensure that each bind point in binding has a result
        self._validate_all_bindings_have_result(results)
        if strict:
            # Ensure that every collected result is bound
            self._validate_all_results_have_binding(results)

    def _validate_binding_spec_compatibility(self, spec: Spec):
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
            if len(self.identifiers_for(property.name)) < 1:
                raise RuntimeError(
                    "Binding must include at least"
                    f" one mapping for property {property.name}."
                )
        for name in self.description.keys():
            if not spec.has_property(name):
                raise RuntimeError(
                    "Binding contains" f" unnecessary property {name}."
                )

    def _validate_all_bindings_have_result(
        self, results: Iterable[ValidationResult]
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
        for property_name, identifiers in self.description.items():
            for identifier in identifiers:
                if identifier not in result_identifiers:
                    raise RuntimeError(
                        f"Missing result to bind to {identifier}"
                        f" for property {property_name}."
                    )

    def _validate_all_results_have_binding(
        self, results: Iterable[ValidationResult]
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
            id for collection in self.description.values() for id in collection
        )
        for result_identifier in result_identifiers:
            if result_identifier not in binding_identifiers:
                raise RuntimeError(
                    f"Result with identifier '{result_identifier}'"
                    " is not bound to any property."
                )

    def _bind_to_property(
        self,
        property: Property,
        results: Iterable[ValidationResult],
    ) -> list[ValidationResult]:
        """
        Collect the results for an individual property
        from result set into a list including only those results.

        :param property: The property of interest
        :type property: Property
        :param results: The collection of results
        :type results: Iterable[ValidationResult]

        :return: A list of the ValidationResults for the given property.
        :rtype: list[ValidationResult]
        """
        assert all(
            r.result is not None for r in results
        ), "Broken precondition."

        # Filter results relevant to property
        targets = set(self.identifiers_for(property.name))
        assert len(targets) > 0, "Broken invariant."

        # TODO(Kyle): Clean this up.
        results_for_property = [
            r for r in results if str(r.result.identifier) in targets  # type: ignore
        ]

        return results_for_property

    def __eq__(self, other: object) -> bool:
        """Compare Binding instances for equality."""
        if not isinstance(other, Binding):
            return False
        return _equal(self, other)

    def __neq__(self, other: object) -> bool:
        """Compare binding instances for inequality."""
        return not self.__eq__(other)


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


def _equal(a: Binding, b: Binding) -> bool:
    """
    Determine if two binding instances are equivalent.

    :param a: Binding instance
    :type a: Binding
    :param b: Binding instance
    :type b: Binding

    :return: `True` if equal, `False` otherwise
    :rtype: bool
    """
    ad = a.description
    bd = b.description

    # Determine if keys are equivalent
    if (
        not len(ad)
        == len(bd)
        == len(set(ad.keys()).intersection(set(bd.keys())))
    ):
        return False

    # Determine if all values are equivalent
    for k in ad.keys():
        assert k in bd.keys(), "Broken invariant."
        if not _list_equal(ad[k], bd[k]):
            return False

    return True


def _list_equal(a: List[str], b: List[str]) -> bool:
    """
    Determine if the contents of two lists are equivalent, ignoring order.

    :param a: List instance
    :type a: List[str]
    :param b: List instance
    :type b: List[str]

    :return: `True` if equal, `False` otherwise
    :rtype: bool
    """
    if not len(a) == len(b):
        return False
    return len(set(a)) == len(set(b)) == len(set(a).intersection(set(b)))
