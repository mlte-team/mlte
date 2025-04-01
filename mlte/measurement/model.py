"""
Model implementation for the Measurement artifact.
"""

from mlte.model.base_model import BaseModel


class MeasurementMetadata(BaseModel):
    """Info about a Measurement."""

    measurement_class: str
    """The module/name of the class used for this measurement."""

    output_class: str
    """The module/class of the output produced by this measurement."""

    additional_data: dict[str, str] = {}
    """Additional metadata to add."""

    def __str__(self) -> str:
        """Return a string representation."""
        representation = (
            f"{self.measurement_class} - output class: {self.output_class}"
        )
        for key, additional_data in self.additional_data.items():
            representation += f"; {key}: {additional_data}"
        return representation
