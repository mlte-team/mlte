"""
mlte/property/property.py

The superclass for all model properties.
"""

from __future__ import annotations

import abc
import importlib
import pkgutil
from typing import Type

import mlte._private.meta as meta
from mlte.spec.model import PropertyModel


class Property(metaclass=abc.ABCMeta):
    """The Property type represents an abstract model property."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return meta.has_callables(subclass, "__init__")

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

        self.description: str = description
        """The description of the property."""

        self.rationale: str = rationale
        """The rationale for using the property."""

    def to_model(self) -> PropertyModel:
        """
        Return a Property as a model.

        :return: The property as its model.
        :rtype: PropertyModel
        """
        return PropertyModel(
            name=self.name,
            description=self.description,
            rationale=self.rationale,
        )

    @classmethod
    def from_model(cls, model: PropertyModel) -> Property:
        """
        Load a Property instance from a model.

        :param model: The model with the Property info.
        :type model: PropertyModel

        :return: The loaded property
        :rtype: Property
        """
        if model.name == "":
            raise RuntimeError(
                "Property is malformed, it does not have a valid name."
            )
        classname = model.name

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
            return class_(model.rationale)  # type: ignore

        raise RuntimeError(f"Property {model.name} not found")
