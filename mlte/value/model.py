"""
mlte/value/model.py

Model implementation for MLTE value types.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Union

from pydantic import Field

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel


class ValueType(str, Enum):
    """An enumeration over supported value types."""

    INTEGER = "integer"
    """An integral type."""

    REAL = "real"
    """A real type."""

    OPAQUE = "opaque"
    """An opaque type."""

    IMAGE = "image"
    """An image media type."""

    ARRAY = "array"
    """An array of values."""


class ValueModel(BaseModel):
    """The model implementation for MLTE values."""

    artifact_type: Literal[ArtifactType.VALUE]
    """Union discriminator."""

    metadata: EvidenceMetadata
    """Evidence metadata associated with the value."""

    value_class: str
    """Full path to class that implements this value."""

    value: Union[
        "IntegerValueModel",
        "RealValueModel",
        "OpaqueValueModel",
        "ImageValueModel",
        "ArrayValueModel",
    ] = Field(..., discriminator="value_type")
    """The body of the value."""


class IntegerValueModel(BaseModel):
    """The model implementation for MLTE integer values."""

    value_type: Literal[ValueType.INTEGER]
    """An identitifier for the value type."""

    integer: int
    """The encapsulated value."""

    class Config:
        use_enum_values = True


class RealValueModel(BaseModel):
    """The model implementation for MLTE real values."""

    value_type: Literal[ValueType.REAL]
    """An identitifier for the value type."""

    real: float
    """The encapsulated value."""

    class Config:
        use_enum_values = True


class OpaqueValueModel(BaseModel):
    """The model implementation for MLTE opaque values."""

    value_type: Literal[ValueType.OPAQUE]
    """An identitifier for the value type."""

    data: Dict[str, Any]
    """Encapsulated, opaque data."""

    class Config:
        use_enum_values = True


class ImageValueModel(BaseModel):
    """The model implementation for MLTE image values."""

    value_type: Literal[ValueType.IMAGE]
    """An identitifier for the value type."""

    data: str
    """The image data as base64-encoded string."""

    class Config:
        use_enum_values = True


class ArrayValueModel(BaseModel):
    """The model implementation for MLTE array values."""

    value_type: Literal[ValueType.ARRAY]
    """An identitifier for the value type."""

    data: List[Any]
    """The array to capture."""

    class Config:
        use_enum_values = True


ValueModel.model_rebuild()
