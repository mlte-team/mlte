"""
mlte/measurement/external_measurement.py

Base class for measurements calculated by external functions.
"""

from __future__ import annotations

import typing
from typing import Any, Callable, Optional

import mlte._private.meta as meta
from mlte._private.reflection import load_class_or_function
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
        test_case_id: Optional[str] = None,
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

        # Set up the output type class.
        self.output_evidence_type = typing.cast(
            type[Evidence], load_class_or_function(model.output_class)
        )

        # Set up the function.
        if self.EXTERNAL_FUNCTION_KEY in model.additional_data:
            self.function = load_class_or_function(
                model.additional_data[self.EXTERNAL_FUNCTION_KEY]
            )

        # Set the metadata.
        self.set_metadata()

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

    def get_output_type(self) -> type[Evidence]:  # type: ignore
        """Object method with proper results, similar to the class level get_output_type method, which will always return Opaque for this class."""
        return self.output_evidence_type

    def __eq__(self, other: object) -> bool:
        """Test instance for equality."""
        if not isinstance(other, ExternalMeasurement):
            return False
        return (
            self.test_case_id == other.test_case_id
            and self.evidence_metadata == other.evidence_metadata
            and self.output_evidence_type == other.output_evidence_type
            and self.function == other.function
        )
