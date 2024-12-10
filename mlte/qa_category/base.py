"""
mlte/qa_category/base.py

The superclass for all model qa categories.
"""

from __future__ import annotations

import abc
import importlib
from typing import Type

import mlte._private.meta as meta
from mlte._private.text import cleantext
from mlte.spec.model import QACategoryModel


class QACategory(metaclass=abc.ABCMeta):
    """The QACategory type represents an abstract model qa category."""

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete quality attribute categories."""
        return meta.has_callables(subclass, "__init__")

    def __init__(
        self,
        instance: QACategory,
        description: str,
        rationale: str,
    ):
        """
        Initialize a QACategory instance.

        :param instance: The derived QACategory we are constructing from.
        :param description: The description of the qa category
        :param rationale: The rationale for using the qa category
        """
        self.name: str = instance.__class__.__name__
        """The name of the qa category."""

        self.description: str = cleantext(description)
        """The description of the qa category."""

        self.rationale: str = rationale
        """The rationale for using the qa category."""

        self.module: str = instance.__module__
        """The name of the module the qa category is defined in."""

    def to_model(self) -> QACategoryModel:
        """
        Return a QACategory as a model.

        :return: The qa category as its model.
        """
        return QACategoryModel(
            name=self.name,
            description=self.description,
            rationale=self.rationale,
            module=self.module,
        )

    @classmethod
    def from_model(
        cls, model: QACategoryModel
    ) -> QACategory:
        """
        Load a QACategory instance from a model.

        :param model: The model with the QACategory info.

        :return: The loaded qa category
        """
        if model.name == "":
            raise RuntimeError(
                "QACategory is malformed, it does not have a valid name."
            )
        classname = model.name

        # Load the class type from the module
        module_path = model.module
        try:
            qa_category_module = importlib.import_module(module_path)
        except Exception:
            raise RuntimeError(f"Module {module_path} not found")
        try:
            class_: Type[QACategory] = getattr(
                qa_category_module, classname
            )
        except AttributeError:
            raise RuntimeError(
                f"QACategory {model.name} in module {module_path} not found"
            )

        # Instantiate the qa category
        return class_(model.rationale)  # type: ignore
