"""
mlte/property/property.py

The superclass for all model properties.
"""

from __future__ import annotations

import abc
import importlib
import pkgutil
from typing import Dict, Type

import mlte._private.meta as meta


class Property(metaclass=abc.ABCMeta):
    """The Property type represents an abstract model property."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return meta.has_callables(subclass, "__init__", "__repr__")

    def __init__(self, name: str, description: str, rationale: str):
        """
        Initialize a Property instance.

        :param name: The name of the property
        :type name: str
        :param description: The description of the property
        :type description: str
        :param rationale: The rationale for using the property
        :type rationale: str
        """
        self.name: str = name
        """The name of the property."""
        self.description = description
        """The description of the property."""
        self.rationale = rationale
        """The rationale for using the property."""

    def _to_json(self) -> Dict[str, str]:
        """
        Save a Property instance to a JSON document.

        :return: The document
        :rtype: Dict[str, str]
        """
        return {
            "name": self.name,
            "repr": repr(self),
            "description": self.description,
            "rationale": self.rationale,
        }

    @staticmethod
    def _from_json(document: Dict[str, str]) -> Property:
        """
        Load a Property instance from a JSON document.

        :param document: The document for the saved property
        :type document: Dict[str, str]

        :return: The loaded property
        :rtype: Property
        """
        return _load_from_document(document)

    def __repr__(self) -> str:
        """Return the representation needed to reconstruct the object."""
        return f"{self.name}()"


def _get_class_name(property_repr: str) -> str:
    """
    Extract the class name from the property representation.

    :param property_repr: The representation
    :type property_repr: str

    :return: The class name
    :rtype: str
    """
    return property_repr[: property_repr.index("(")]


def _load_from_document(document: Dict[str, str]) -> Property:
    """
    Load a Property instance from its identifier.

    :param name: The name of the property
    :type name: str

    :return: The loaded property
    :rtype: Property
    """
    if "name" not in document or "repr" not in document:
        raise RuntimeError("Saved property is malformed.")
    property_repr = document["repr"]
    rationale = document["rationale"]

    # Extract the classname from the call
    classname = _get_class_name(property_repr)

    # Load the class type from the module
    properties_package_name = "mlte.property"
    properties_module = importlib.import_module(
        properties_package_name, package="mlte"
    )
    for submodule_info in pkgutil.iter_modules(
        properties_module.__path__, properties_module.__name__ + "."
    ):
        submodule = importlib.import_module(
            submodule_info.name, package=properties_package_name
        )
        try:
            class_: Type[Property] = getattr(submodule, classname)
        except AttributeError:
            continue

        # Instantiate the property
        return class_(rationale)  # type: ignore

    raise RuntimeError(f"Property {document['name']} not found")
