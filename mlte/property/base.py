"""
mlte/property/base.py

The superclass for all model properties.
"""

from __future__ import annotations

import abc
import importlib
from typing import Type

import mlte._private.meta as meta
from mlte._private.text import cleantext
from mlte.spec.model import PropertyModel


class Property(metaclass=abc.ABCMeta):
    """The Property type represents an abstract model property."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete properties."""
        return meta.has_callables(subclass, "__init__")

    def __init__(self, instance: Property, description: str, rationale: str):
        """
        Initialize a Property instance.

        :param instance: The derived Property we are constructing from.
        :param description: The description of the property
        :param rationale: The rationale for using the property
        """
        self.name: str = instance.__class__.__name__
        """The name of the property."""

        self.description: str = cleantext(description)
        """The description of the property."""

        self.rationale: str = rationale
        """The rationale for using the property."""

        self.module: str = instance.__module__
        """The name of the module the property is defined in."""

    def to_model(self) -> PropertyModel:
        """
        Return a Property as a model.

        :return: The property as its model.
        """
        return PropertyModel(
            name=self.name,
            description=self.description,
            rationale=self.rationale,
            module=self.module,
        )

    @classmethod
    def from_model(cls, model: PropertyModel) -> Property:
        """
        Load a Property instance from a model.

        :param model: The model with the Property info.

        :return: The loaded property
        """
        if model.name == "":
            raise RuntimeError(
                "Property is malformed, it does not have a valid name."
            )
        classname = model.name

        # Load the class type from the module
        module_path = model.module
        try:
            properties_module = importlib.import_module(module_path)
        except Exception:
            raise RuntimeError(f"Module {module_path} not found")
        try:
            class_: Type[Property] = getattr(properties_module, classname)
        except AttributeError:
            raise RuntimeError(
                f"Property {model.name} in module {module_path} not found"
            )

        # Instantiate the property
        return class_(model.rationale)  # type: ignore
