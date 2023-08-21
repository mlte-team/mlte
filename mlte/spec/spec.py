"""
mlte/spec/spec.py

A collection of properties and their measurements.
"""

from __future__ import annotations

import time
import typing
from typing import Any, Union, List, Dict

from mlte.artifact.artifact import Artifact
from mlte.artifact.type import ArtifactType
from mlte.artifact.model import ArtifactModel, ArtifactHeaderModel
from mlte.property import Property
from mlte._private.schema import SPEC_LATEST_SCHEMA_VERSION
from mlte.session import session
from .requirement import Requirement
from mlte.spec.model import SpecModel, SpecMetadataModel, PropertyModel


def _unique(collection: List[str]) -> bool:
    """
    Determine if all elements of a collection are unique.

    :param collection: The collection
    :type collection: List[str]

    :return: `True` if all elements are unique, `False` otherwise
    :rtype: bool
    """
    return len(set(collection)) == len(collection)


# -----------------------------------------------------------------------------
# Spec
# -----------------------------------------------------------------------------


class Spec(Artifact):
    """
    The Spec class integrates properties, measurements,
    and the results of measurement evaluation and validation.
    """

    def __init__(
        self, identifier: str, properties: Dict[Property, List[Requirement]]
    ):
        """
        Initialize a Spec instance.

        :param properties: The collection of properties that compose the spec.
        :type properties: List[Property]
        """
        identifier = "specification"
        super().__init__(identifier, ArtifactType.SPEC)

        self.properties = [p for p in properties.keys()]
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties]):
            raise RuntimeError("All properties in Spec must be unique.")

        if not _unique(
            [
                str(requirement.identifier)
                for _, req_list in properties.items()
                for requirement in req_list
            ]
        ):
            raise RuntimeError("All requirement ids in Spec must be unique.")

        self.requirements: Dict[str, List[Requirement]] = {
            property.name: properties[property] for property in self.properties
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
    # Serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """Convert a negotation card artifact to its corresponding model."""
        return ArtifactModel(
            header=ArtifactHeaderModel(
                identifier=self.identifier,
                type=self.type,
            ),
            body=SpecModel(
                artifact_type=ArtifactType.SPEC,
                properties=[
                    PropertyModel(**prop)
                    for prop in self._properties_document()
                ],
            ),
        )

    @classmethod
    def from_model(cls, model: ArtifactModel) -> Spec:  # type: ignore[override]
        """Convert a negotiation card model to its corresponding artifact."""
        assert model.header.type == ArtifactType.SPEC, "Broken precondition."
        body = typing.cast(SpecModel, model.body)
        return Spec(
            identifier=model.header.identifier,
            properties=body.properties,
        )

    def to_json(self) -> Dict[str, Any]:
        """
        Serialize Spec content to JSON-like dict document

        :return: The serialized content
        :rtype: Dict[str, Any]
        """
        document = {
            "schema_version": SPEC_LATEST_SCHEMA_VERSION,
            "metadata": self._metadata_document(),
            "properties": self._properties_document(),
        }
        return document

    @staticmethod
    def from_json(json: Dict[str, Any]) -> Spec:
        """
        Deserialize Spec content from JSON document.

        :param json: The json document
        :type json: Dict[str, Any]

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

    def _metadata_document(self) -> Dict[str, Any]:
        """
        Generate Spec metadata.

        :return: The metadata document
        :rtype: Dict[str, Any]
        """
        sesh = session()
        return {
            "namespace": sesh.context.namespace,
            "model": sesh.context.model,
            "version": sesh.context.version,
            "timestamp": int(time.time()),
        }

    def _properties_document(self) -> List[Dict[str, Any]]:
        """
        Generates a document with info an all properties.

        :return: The properties document
        :rtype: Dict[str, Any]
        """
        property_docs = [
            self._property_document(property) for property in self.properties
        ]
        return property_docs

    def _property_document(self, property: Property) -> Dict[str, Any]:
        """
        Generate a property document.

        :param property: The property of interest
        :type property: Property

        :return: The property-level document
        :rtype: Dict[str, Any]
        """
        document: Dict[str, Any] = property._to_json()
        document["requirements"] = [
            requirement.to_json()
            for requirement in self.requirements[property.name]
        ]
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
