"""
A collection of properties and their measurements.
"""

from __future__ import annotations

import time
from typing import Any, Union, Optional

from mlte.property import Property
from mlte.validation import Result
from mlte._private.schema import SPEC_LATEST_SCHEMA_VERSION
from mlte._global import global_state
from mlte.api import read_spec, write_spec
from .validated_spec import ValidatedSpec
from .requirement import Requirement


def _unique(collection: list[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: list[str]

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


# -----------------------------------------------------------------------------
# Spec
# -----------------------------------------------------------------------------


class Spec:
    """
    The Spec class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(
        self, requirements_by_property: dict[Property, list[Requirement]]
    ):
        """
        Initialize a Spec instance.

        :param properties: The collection of properties that compose the spec.
        :type properties: list[Property]
        """
        self.properties = [p for p in requirements_by_property.keys()]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

        if not _unique(
            [
                str(requirement.identifier)
                for _, req_list in requirements_by_property.items()
                for requirement in req_list
            ]
        ):
            raise RuntimeError("All requirement ids in Spec must be unique.")

        self.requirements: dict[str, list[Requirement]] = {
            property.name: requirements_by_property[property]
            for property in self.properties
        }
        """A dict to store requirements by property."""

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

    def _add_requirement(self, property_name: str, requirement: Requirement):
        """
        Adds the given requirement to the property.

        :param property_name: The name of the property we are adding the requirement for.
        :type property_name: str

        :param requirement: The requirement we want to add to this property.
        :type requirement: Requirement
        """
        if not any(
            property.name == property_name for property in self.properties
        ):
            raise RuntimeError(
                f"Property {property_name} is not part of this Specification."
            )
        if property_name not in self.requirements:
            self.requirements[property_name] = []

        # Only add requirement if it is not already there for this property.
        found = any(
            curr_requirement == requirement
            for curr_requirement in self.requirements[property_name]
        )
        if not found:
            self.requirements[property_name].append(requirement)

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
            for requirement_doc in property_doc["requirements"]:
                spec._add_requirement(
                    property_doc["name"], Requirement.from_json(requirement_doc)
                )

        return spec

    def _spec_document(
        self,
        results: Optional[dict[str, Result]] = None,
    ) -> dict[str, Any]:
        """
        Generate the spec document.

        :param result: The Results of validations, ordered by id (optional).
        :type results: dict[str, Result]

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
        results: Optional[dict[str, Result]] = None,
    ) -> list[dict[str, Any]]:
        """
        Generates a document with info an all properties.

        :param result: The Results of validations, ordered by id (optional).
        :type results: dict[str, Result]

        :return: The properties document
        :rtype: dict[str, Any]
        """
        property_docs = [
            self._property_document(
                property,
                results if results is not None else {},
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
        :param result: The Results of validations, ordered by id.
        :type results: dict[str, Result]

        :return: The property-level document
        :rtype: dict[str, Any]
        """
        document: dict[str, Any] = property._to_json()
        document["requirements"] = self._requirements_document(
            self.requirements[property.name], results
        )
        return document

    def _requirements_document(
        self,
        requirements: list[Requirement],
        results: dict[str, Result],
    ) -> list[dict[str, Any]]:
        """
        Generate a requirements document.

        :param requirements: A list of Requirements.
        :type requirements: list[Requirement]
        :param result: The optional Results of validations, ordered by requirement.
        :type results: dict[str, Result]

        :return: The requirements-level document
        :rtype: list[dict[str, Any]]
        """
        document = [
            self._requirement_document(
                requirement,
                results[str(requirement.identifier)]
                if str(requirement.identifier) in results
                else None,
            )
            for requirement in requirements
        ]
        return document

    def _requirement_document(
        self,
        requirement: Requirement,
        result: Optional[Result] = None,
    ) -> dict[str, Any]:
        """
        Returns a document with information for a given requirement, optionally with validation result.

        :param requirement: The requirement to turn into a document.
        :type requirement: Requirement
        :param result: The Result of validating the Requirement, if any.
        :type result: Optional[Result]

        :return: The document for the specific requirement.
        :rtype: dict[str, Any]
        """
        document = requirement.to_json()
        if result is not None:
            document["result"] = result.to_json()
        return document

    # -------------------------------------------------------------------------
    # ValidatedSpec document generation.
    # -------------------------------------------------------------------------

    def generate_validatedspec(
        self, results: dict[str, Result]
    ) -> ValidatedSpec:
        """
        Generates a validated spec with the validation results.

        :param result: The Results to validate to the spec, ordered by id.
        :type results: str, dict[str, Result]

        :return: A ValidatedSpec associating the Spec with the specific Results.
        :rtype: ValidatedSpec
        """
        if results is None or len(results) == 0:
            raise RuntimeError("Can't generate validated spec without results.")

        # Check that all requirements have results.
        for _, requirement_list in self.requirements.items():
            for requirement in requirement_list:
                if str(requirement.identifier) not in results:
                    raise RuntimeError(
                        f"Requirement '{requirement.identifier}' does not have a result."
                    )

        return ValidatedSpec(self._spec_document(results))

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
