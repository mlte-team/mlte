"""
mlte/spec/spec.py

A collection of properties and their measurements.
"""

from __future__ import annotations

import typing
from typing import Dict, List, Union

from mlte.artifact.artifact import Artifact
from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.property.base import Property
from mlte.spec.condition import Condition
from mlte.spec.model import PropertyModel, SpecModel

DEFAULT_SPEC_ID = "default.spec"


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
        self,
        identifier: str = DEFAULT_SPEC_ID,
        properties: Dict[Property, Dict[str, Condition]] = {},
    ):
        """
        Initialize a Spec instance.

        :param properties: The collection of properties that compose the spec, with their conditions keyed by measurement id.
        :type properties: List[Property]
        """
        super().__init__(identifier, ArtifactType.SPEC)

        self.properties = properties
        """The collection of properties that compose the Spec."""

        if not _unique([p.name for p in self.properties.keys()]):
            raise RuntimeError("All properties in Spec must be unique.")

    # -------------------------------------------------------------------------
    # Serialization.
    # -------------------------------------------------------------------------

    def to_model(self) -> ArtifactModel:
        """Convert a negotation card artifact to its corresponding model."""
        return ArtifactModel(
            header=self.build_artifact_header(),
            body=SpecModel(
                artifact_type=ArtifactType.SPEC,
                properties=[
                    self._to_property_model(property)
                    for property, _ in self.properties.items()
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
            properties={
                Property.from_model(property_model): {
                    measurement_id: Condition.from_model(condition_model)
                    for measurement_id, condition_model in property_model.conditions.items()
                }
                for property_model in body.properties
            },
        )

    def _to_property_model(self, property: Property) -> PropertyModel:
        """
        Generate a property model. This just uses Property.to_model, but adds the list of conditions.

        :param property: The property of interest
        :type property: Property

        :return: The property model
        :rtype: PropertyModel
        """
        property_model: PropertyModel = property.to_model()
        property_model.conditions = {
            measurement_id: condition.to_model()
            for measurement_id, condition in self.properties[property].items()
        }
        return property_model

    @staticmethod
    def get_default_id() -> str:
        """Overriden"""
        return DEFAULT_SPEC_ID

    # -------------------------------------------------------------------------
    # Property Manipulation
    # -------------------------------------------------------------------------

    def get_property(self, property_id: str) -> Property:
        """
        Returns a particular property with the given id.

        :param property_id: The property itself, or its identifier
        :type property_id: str

        :return: The property object.
        :rtype: Property
        """
        properties = [
            prop for prop in self.properties if prop.name == property_id
        ]
        if len(properties) == 0:
            raise RuntimeError(f"Property {property_id} was not found in list.")
        if len(properties) > 1:
            raise RuntimeError(
                f"Multiple properties with same id were found: {property_id}"
            )
        return properties[0]

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
    same_props = all(b.has_property(p) for p in a.properties) and all(
        a.has_property(p) for p in b.properties
    )
    same_conditions = all(
        a.properties[prop] == b.properties[b.get_property(prop.name)]
        for prop in a.properties
    )
    return a.identifier == b.identifier and same_props and same_conditions
