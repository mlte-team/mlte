"""
mlte/value/model.py

Model implementation for MLTE value types.
"""

from enum import Enum, auto
from typing import Any, Literal, Union

from pydantic import Field

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel


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

    artifact_type: Literal[ArtifactType.VALUE]
    """Union discriminator."""

    metadata: EvidenceMetadata
    """Evidence metadata associated with the value."""

    value: Union[
        "IntegerValueModel",
        "RealValueModel",
        "OpaqueValueModel",
        "ImageValueModel",
    ] = Field(..., discriminator="value_type")
    """The body of the value."""


class IntegerValueModel(BaseModel):
    """The model implementation for MLTE integer values."""

    value_type: Literal[ValueType.INTEGER]
    """An identitifier for the value type."""

    integer: int
    """The encapsulated value."""


class RealValueModel(BaseModel):
    """The model implementation for MLTE real values."""

    value_type: Literal[ValueType.REAL]
    """An identitifier for the value type."""

    real: float
    """The encapsulated value."""


class OpaqueValueModel(BaseModel):
    """The model implementation for MLTE opaque values."""

    value_type: Literal[ValueType.OPAQUE]
    """An identitifier for the value type."""

    data: dict[str, Any]
    """Encapsulated, opaque data."""


class ImageValueModel(BaseModel):
    """The model implementation for MLTE image values."""

    value_type: Literal[ValueType.IMAGE]
    """An identitifier for the value type."""

    data: str
    """The image data as base64-encoded string."""


ValueModel.update_forward_refs()
