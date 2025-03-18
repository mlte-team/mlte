"""
mlte/measurement/external_measurement.py

Base class for measurements calculated by external functions.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

import mlte._private.meta as meta
from mlte._private.reflection import load_class
from mlte.evidence.artifact import Evidence
from mlte.evidence.types.opaque import Opaque
from mlte.measurement.measurement import Measurement
from mlte.measurement.model import MeasurementMetadata


class ExternalMeasurement(Measurement):
    """Base measurement class when the evaluated function is an external function."""

    EXTERNAL_FUNCTION_KEY = "function"
    """Key to store external function used by this measurement."""

    def __init__(
        self,
        test_case_id: str,
        output_evidence_type: type[Evidence] = Opaque,
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
    def additional_setup(self, model: MeasurementMetadata):
        """Optional method to be overriden by subclasses needing additional setup from metadata."""
        self.output_evidence_type = load_class(model.output_class)

    # Overriden.
    def generate_metadata(self) -> MeasurementMetadata:
        """Returns Measurement metadata with additional info."""
        metadata = super().generate_metadata()

        # Override default class with external-measurement specific one.
        metadata.output_class = meta.get_qualified_name(
            self.output_evidence_type
        )

        # Add specific function being used.
        if self.function is not None:
            metadata.additional_data[self.EXTERNAL_FUNCTION_KEY] = (
                meta.get_qualified_name(self.function)
            )
        return metadata

    # Overriden.
    def __call__(self, *args, **kwargs) -> Evidence:
        """Evaluate a measurement and return values without semantics."""
        evidence: Evidence
        if self.function is None:
            # If no function is configured, we just want to wrap the results in the Evidence type.
            evidence = self.output_evidence_type(*args, **kwargs)
        else:
            evidence = self.output_evidence_type(self.function(*args, **kwargs))
        return evidence

    # Overriden.
    def get_output_type(self) -> type[Evidence]:
        return self.output_evidence_type
