"""
mlte/measurement/measurement.py

Superclass for all measurements.
"""

from __future__ import annotations

import typing
from abc import ABC, abstractmethod
from typing import Optional, Type

import mlte._private.meta as meta
from mlte._private.reflection import load_class
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.measurement.model import MeasurementModel
from mlte.model.base_model import BaseModel
from mlte.model.serializable import Serializable
from mlte.value.artifact import Value
from mlte.value.types.opaque import Opaque


class Measurement(Serializable, ABC):
    """
    The superclass for all model measurements.
    """

    # -------------------------------------------------------------------------
    # Constructor.
    # -------------------------------------------------------------------------

    def __init__(
        self,
        identifier: str,
        function: Optional[str] = None,
    ):
        """
        Initialize a new Measurement instance.

        :param instance: The invoking instance (Measurement subclass)
        :param identifier: A unique identifier for the instance
        """
        self.metadata = EvidenceMetadata(
            measurement_type=meta.get_class_path(self.__class__),
            identifier=Identifier(name=identifier),
            function=function,
        )
        """The metadata for the measurement instance."""

    # -------------------------------------------------------------------------
    # Measurement interface definition.
    # -------------------------------------------------------------------------

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete measurements."""
        return meta.has_callables(subclass, "__call__")

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Value:
        """Evaluate a measurement and return a value semantics."""
        raise NotImplementedError("Cannot evaluate abstract measurement.")

    # -------------------------------------------------------------------------
    # Base methods.
    # -------------------------------------------------------------------------

    def evaluate(self, *args, **kwargs) -> Value:
        """
        Evaluate a measurement and return a value with semantics.

        :return: The resulting value of measurement execution, with semantics
        :rtype: Value
        """
        # Evaluate the measurement
        return self.__call__(*args, **kwargs)

    @classmethod
    def value(cls) -> Type[Value]:
        """Returns the class type object for the Value produced by the Measurement."""
        # Opaque is the default Value type.
        return Opaque

    def __str__(self) -> str:
        """Return a string representation of a Measurement."""
        return f"{self.metadata}"

    # -------------------------------------------------------------------------
    # Model handling.
    # -------------------------------------------------------------------------

    def to_model(self) -> MeasurementModel:
        """
        Returns this validator as a model.

        :return: The serialized model object.
        """
        return MeasurementModel(
            measurement_class=meta.get_class_path(self),
            measurement_function=self.metadata.function,
            output_class=meta.get_class_path(self.value()),
        )

    @classmethod
    def from_model(cls, model: BaseModel) -> Measurement:
        """
        Deserialize a Validator from a model.

        :param model: The model.

        :return: The deserialized Validator
        """
        model = typing.cast(MeasurementModel, model)
        measurement_class: Type[Measurement] = load_class(
            model.measurement_class
        )

        # TODO: figure out how to change identifier and instance cases to make this actually load
        measurement: Measurement = measurement_class(
            "", model.measurement_function
        )
        return measurement

    # -------------------------------------------------------------------------
    # Equality Testing
    # -------------------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Measurement):
            return False
        return self._equal(other)
