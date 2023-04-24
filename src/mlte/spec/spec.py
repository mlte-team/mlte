"""
A collection of properties and their measurements.
"""

from __future__ import annotations

import time
from itertools import groupby
from typing import Iterable, Any, Union, Type, Optional

from mlte.property import Property
from mlte.validation import Result
from mlte._private.schema import SPEC_LATEST_SCHEMA_VERSION
from mlte._global import global_state
from mlte.store.api import read_spec, write_spec
from .bound_spec import BoundSpec
from .condition import Condition
from mlte.measurement import Measurement


def _unique(collection: list[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: list[str]

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

    def __init__(self, properties: dict[Property, list[Condition]]):
        """
        Initialize a Spec instance. Only one of the two arguments should be provided, not both.

        :param properties: The collection of properties that compose the spec.
        :type conditions: list[Property]
        """
        self.properties = [p for p in properties.keys()]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

        self.conditions: dict[str, list[Condition]] = {
            property.name: properties[property] for property in self.properties
        }
        """A dict to store conditions by property."""

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

    def add_condition(
        self,
        property_name: str,
        label: str,
        measurement_type: Type[Measurement],
        validator: str,
        threshold: Any,
    ):
        """
        Adds a condition for the given property, with information from a measurement, plus additional condition info.

        :param property_name: The name of the property we are adding the condition for.
        :type property_name: str

        :param label: The name to give the condition to track it.
        :type label: str

        :param measurement: The type measurement we are want to have in the condition.
        :type measurement: Type

        :param validator: The validator method for the condition.
        :type validator: str

        :param threshold: The threshold value for the validation.
        :type threshold: Any
        """
        condition = Condition(
            label, measurement_type.__name__, validator, threshold
        )
        self._add_condition(property_name, condition)

    def _add_condition(self, property_name: str, condition: Condition):
        """
        Adds the given condition to the property.

        :param property_name: The name of the property we are adding the condition for.
        :type property_name: str

        :param condition: The condition we want to add to this property.
        :type condition: Condition
        """
        if not any(
            property.name == property_name for property in self.properties
        ):
            raise RuntimeError(
                f"Property {property_name} is not part of this Specification."
            )
        if property_name not in self.conditions:
            self.conditions[property_name] = []

        # Only add condition if it is not already there for this property.
        found = any(
            curr_condition == condition
            for curr_condition in self.conditions[property_name]
        )
        if not found:
            self.conditions[property_name].append(condition)

    # -------------------------------------------------------------------------
    # Save / Load
    # -------------------------------------------------------------------------

    def save(self):
        """Persist the specification to artifact store."""
        state = global_state()
        state.ensure_initialized()

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
        state.ensure_initialized()

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
        return self._spec_document()

    @staticmethod
    def _from_json(json: dict[str, Any]) -> Spec:
        """
        Deserialize Spec content from JSON document.

        :param json: The json document
        :type json: dict[str, Any]

        :return: The deserialized specification
        :rtype: Spec
        """
        spec = Spec({Property._from_json(d): [] for d in json["properties"]})
        for property_doc in json["properties"]:
            for measurement_doc in property_doc["measurements"]:
                for condition_doc in measurement_doc["conditions"]:
                    spec._add_condition(
                        property_doc["name"], Condition.from_json(condition_doc)
                    )

        return spec

    def _spec_document(
        self,
        results: Optional[dict[str, dict[str, Result]]] = None,
    ) -> dict[str, Any]:
        """
        Generate the spec document.

        :param result: The Results of validations, ordered by property and condition (optional).
        :type results: dict[str, dict[str, Result]]

        :return: The spec document
        :rtype: dict[str, Any]
        """
        document = {
            "schema_version": SPEC_LATEST_SCHEMA_VERSION,
            "metadata": self._metadata_document(),
            "properties": self._properties_document(results),
        }
        return document

    def _metadata_document(self) -> dict[str, Any]:
        """
        Generate Spec metadata.

        :return: The metadata document
        :rtype: dict[str, Any]
        """
        state = global_state()
        state.ensure_initialized()
        model_identifier, model_version = state.get_model()
        return {
            "model_identifier": model_identifier,
            "model_version": model_version,
            "timestamp": int(time.time()),
        }

    def _properties_document(
        self,
        results: Optional[dict[str, dict[str, Result]]] = None,
    ) -> list[dict[str, Any]]:
        """
        Generates a document with info an all properties.

        :param result: The Results of validations, ordered by property and condition (optional).
        :type results: dict[str, dict[str, Result]]

        :return: The properties document
        :rtype: dict[str, Any]
        """
        if results is not None:
            if any(
                property.name not in results for property in self.properties
            ):
                raise RuntimeError(
                    "There are properties that do not have associated validated results; can't generate document."
                )

        property_docs = [
            self._property_document(
                property,
                results[property.name] if results is not None else {},
            )
            for property in self.properties
        ]
        return property_docs

    def _property_document(
        self, property: Property, results: dict[str, Result]
    ) -> dict[str, Any]:
        """
        Generate a property document.

        :param property: The property of interest
        :type property: Property
        :param result: The Results of validations, ordered by condition.
        :type results: dict[str, Result]

        :return: The property-level document
        :rtype: dict[str, Any]
        """
        document: dict[str, Any] = property._to_json()
        document["measurements"] = self._measurements_document(
            self.conditions[property.name], results
        )
        return document

    def _measurements_document(
        self,
        conditions: list[Condition],
        results: dict[str, Result],
    ) -> list[dict[str, Any]]:
        """
        Generate a measurements document.

        :param conditions: A list of Conditions.
        :type conditions: list[Condition]
        :param result: The Results of validations, ordered by condition.
        :type results: dict[str, Result]

        :return: The measurements/conditions-level document
        :rtype: list[dict[str, Any]]
        """
        conditions_by_measurement = []
        for _, group in groupby(
            conditions, key=lambda condition: condition.measurement_type
        ):
            conditions_by_measurement.append([condition for condition in group])

        document = [
            self._measurement_document(conditions, results)
            for conditions in conditions_by_measurement
        ]
        return document

    def _measurement_document(
        self,
        conditions: list[Condition],
        results: dict[str, Result],
    ) -> dict[str, Any]:
        """
        Returns a document with information for a measurement type.

        :param conditions: A list of Conditions to add.
        :type conditions: list[Condition]
        :param result: The Results of validations, ordered by condition.
        :type results: dict[str, Result]

        :return: The document for a specific measurement.
        :rtype: dict[str, Any]
        """
        assert len(conditions) > 0, "Broken invariant."
        assert _all_equal(
            condition.measurement_type for condition in conditions  # type: ignore
        ), "Broken invariant."

        measurement_type = conditions[0].measurement_type  # type: ignore

        # Proper results are obtained form the condition label.
        document = {
            "measurement_type": measurement_type,
            "conditions": [
                self._condition_document(
                    condition,
                    results[condition.label]
                    if condition.label in results
                    else None,
                )
                for condition in conditions
            ],
        }
        return document

    def _condition_document(
        self,
        condition: Condition,
        result: Optional[Result] = None,
    ) -> dict[str, Any]:
        """
        Returns a document with information for a given condition, optionally with validation result.

        :param condition: The condition to turn into a document.
        :type condition: Condition
        :param result: The Result of validating the Condition, if any.
        :type result: Optional[Result]

        :return: The document for the specific condition.
        :rtype: dict[str, Any]
        """
        document = condition.to_json()
        if result is not None:
            document["validation"] = result.to_json()
        return document

    # -------------------------------------------------------------------------
    # BoundSpec document generation.
    # -------------------------------------------------------------------------

    def generate_bound_spec(
        self, results: dict[str, dict[str, Result]]
    ) -> BoundSpec:
        """
        Generates a bound spec with the validation results.

        :param result: The Results to bind to the spec, ordered by property and condition.
        :type results: dict[str, dict[str, Result]]

        :return: A BoundSpec associating the Spec with the specific Results.
        :rtype: BoundSpec
        """
        return BoundSpec(self._spec_document(results))

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
