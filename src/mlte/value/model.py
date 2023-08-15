"""
mlte/value/model.py

Model implementation for MLTE value types.
"""

from enum import Enum, auto
from typing import Union, Any
from mlte.model import BaseModel
from mlte.evidence.metadata import EvidenceMetadata


class ValueType(str, Enum):
    """An enumeration over supported value types."""

    INTEGER = auto()
    """An integral type."""

    REAL = auto()
    """A real type."""

    OPAQUE = auto()
    """An opaque type."""

    IMAGE = auto()
    """An image media type."""


class ValueModel(BaseModel):
    """The model implementation for MLTE values."""

    type: ValueType
    """An identitifier for the value type."""

    metadata: EvidenceMetadata
    """Evidence metadata associated with the value."""

    value: Union[
        "IntegerValueModel",
        "RealValueModel",
        "OpaqueValueModel",
        "ImageValueModel",
    ]
    """The body of the value."""


class IntegerValueModel(BaseModel):
    """The model implementation for MLTE integer values."""

    integer: int
    """The encapsulated value."""


class RealValueModel(BaseModel):
    """The model implementation for MLTE real values."""

    real: float
    """The encapsulated value."""


class OpaqueValueModel(BaseModel):
    """The model implementation for MLTE opaque values."""

    data: dict[str, Any]
    """Encapsulated, opaque data."""


class ImageValueModel(BaseModel):
    """The model implementation for MLTE image values."""

    data: str
    """The image data as base64-encoded string."""
