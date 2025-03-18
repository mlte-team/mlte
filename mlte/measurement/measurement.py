"""
Superclass for all measurements.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import mlte._private.meta as meta
from mlte._private.reflection import load_class
from mlte.evidence.artifact import Evidence
from mlte.evidence.metadata import EvidenceMetadata
from mlte.evidence.types.opaque import Opaque
from mlte.measurement.model import MeasurementMetadata


class Measurement(ABC):
    """
    The superclass for all model measurements.
    """

    def __init__(self, test_case_id: str):
        """Constructor."""
        # Set our id to the test case id, and generate our evidence metadata.
        self.set_test_case_id(test_case_id)

    def set_test_case_id(self, test_case_id: str):
        # Set the given test case id and update our metadata.

        self.test_case_id = test_case_id
        """The id of the test case this measurement is for."""

        self.set_evidence_metadata()
        """Metadata to be used on any Evidence generated by the Measurement."""

    def set_evidence_metadata(self):
        """Resets the internal metadata to associate to Evidences generated by this measurement."""
        self.evidence_metadata = EvidenceMetadata(
            test_case_id=self.test_case_id, measurement=self.generate_metadata()
        )

    # -------------------------------------------------------------------------
    # Measurement interface definition.
    # -------------------------------------------------------------------------

    @classmethod
    def __subclasshook__(cls, subclass):
        """Define the interface for all concrete measurements."""
        return meta.has_callables(subclass, "__call__")

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Evidence:
        """Evaluate a measurement and return a value semantics."""
        raise NotImplementedError("Cannot evaluate abstract measurement.")

    # -------------------------------------------------------------------------
    # Base methods.
    # -------------------------------------------------------------------------

    def evaluate(self, *args, **kwargs) -> Evidence:
        """
        Evaluate a measurement and return a value with semantics.

        :return: The resulting value of measurement execution, with semantics
        :rtype: Evidence
        """
        # Evaluate the measurement
        return self.__call__(*args, **kwargs).with_metadata(
            self.evidence_metadata
        )

    def get_output_type(self) -> type[Evidence]:
        """Returns the class type object for the Evidence produced by the Measurement."""
        # Opaque is the default Evidence type.
        return Opaque

    # -------------------------------------------------------------------------
    # MeasurementMetadata model handling.
    # -------------------------------------------------------------------------

    def generate_metadata(self) -> MeasurementMetadata:
        """Returns Measurement metadata."""
        return MeasurementMetadata(
            measurement_class=meta.get_qualified_name(self.__class__),
            output_class=meta.get_qualified_name(self.get_output_type()),
        )

    @classmethod
    def from_metadata(
        cls, model: MeasurementMetadata, test_case_id: str
    ) -> Measurement:
        """
        Create a Measurement from a model.

        :param model: The MeasurementMetadata model.
        :param test_case_id: The id of the associated test case.
        :return: The Measurement.
        """
        meas_class: type[Measurement] = load_class(model.measurement_class)
        measurement = meas_class(test_case_id)
        measurement.additional_setup(model)
        return measurement

    def additional_setup(self, model: MeasurementMetadata):
        """Optional method to be overriden by subclasses needing additional setup from metadata."""
        return

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a string representation of a Measurement."""
        return str(self.generate_metadata())

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, Measurement):
            return False
        return (
            self.test_case_id == other.test_case_id
            and self.evidence_metadata == self.evidence_metadata
        )
