"""
mlte/measurement/external_measurement.py

Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Type

from mlte._private.meta import get_full_path
from mlte.evidence.artifact import Evidence
from mlte.measurement.measurement import Measurement
from mlte.measurement.model import MeasurementMetadata


class ExternalMeasurement(Measurement):
    """Base measurement class when the evaluated function is an external function."""

    EXTERNAL_FUNCTION_KEY = "function"
    """Key to store external function used by this measurement."""

    def __init__(
        self,
        test_case_id: str,
        output_evidence_type: type,
        function: Optional[Callable[..., Any]] = None,
    ):
        """
        Initialize a new ExternalMeasurement measurement.

        :param test_case_id: A unique identifier for the instance
        :param output_evidence_type: The type of the Evidence this measurement will return.
        :param function: The function to be used when evaluating.
        """
        if not issubclass(output_evidence_type, Evidence):
            raise Exception(
                f"Evidence type provided is not a subtype of Evidence: {output_evidence_type}"
            )
        self.output_evidence_type: type = output_evidence_type
        """The output Evidence type that calls to evaluate will return."""

        self.function: Optional[Callable[..., Any]] = function
        """Store the callable function itself."""

        # Call base constructor.
        super().__init__(test_case_id=test_case_id)

    # Overriden.
    def generate_metadata(self) -> MeasurementMetadata:
        """Returns Measurement metadata with additional info."""
        metadata = super().generate_metadata()
        metadata.additional_data[self.EXTERNAL_FUNCTION_KEY] = get_full_path(
            self.function
        )
        return metadata

    def __call__(self, *args, **kwargs) -> Evidence:
        """Evaluate a measurement and return values without semantics."""
        if self.function is None:
            raise Exception("Can't evaluate, no function was set.")

        evidence: Evidence = self.output_evidence_type(
            self.function(*args, **kwargs)
        )
        return evidence

    def ingest(self, *args, **kwargs) -> Evidence:
        """Ingest data without evaluating a function, to wrap it as the configured Evidence type. Currently works the same as evaluate()."""
        evidence: Evidence = self.output_evidence_type(*args, **kwargs)
        return evidence

    @classmethod
    def output_evidence(self) -> Type[Evidence]:
        """Returns the class type object for the Evidence produced by the Measurement."""
        return self.output_evidence_type
