"""
EvidenceMetadata class definition.
"""

from __future__ import annotations

from mlte.measurement.model import MeasurementMetadata
from mlte.model.base_model import BaseModel


class EvidenceMetadata(BaseModel):
    """A simple wrapper model for evidence metadata."""

    test_case_id: str
    """The identifier of the test case this evidence is associated to."""

    measurement: MeasurementMetadata
    """Information about the measurement used to get this evidence."""

    def __str__(self) -> str:
        """Return a string representation of a EvidenceMetadata."""
        return f"Id: {self.test_case_id} - {self.measurement}"
