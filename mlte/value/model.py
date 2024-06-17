"""
mlte/value/model.py

Model implementation for MLTE value types.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Union

from pydantic import Field
from strenum import StrEnum

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel


class ValueType(StrEnum):
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

    artifact_type: Literal[ArtifactType.VALUE] = ArtifactType.VALUE
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

    value_type: Literal[ValueType.INTEGER] = ValueType.INTEGER
    """An identitifier for the value type."""

    integer: int
    """The encapsulated value."""


class RealValueModel(BaseModel):
    """The model implementation for MLTE real values."""

    value_type: Literal[ValueType.REAL] = ValueType.REAL
    """An identitifier for the value type."""

    real: float
    """The encapsulated value."""


class OpaqueValueModel(BaseModel):
    """The model implementation for MLTE opaque values."""

    value_type: Literal[ValueType.OPAQUE] = ValueType.OPAQUE
    """An identitifier for the value type."""

    data: Dict[str, Any]
    """Encapsulated, opaque data."""


class ImageValueModel(BaseModel):
    """The model implementation for MLTE image values."""

    value_type: Literal[ValueType.IMAGE] = ValueType.IMAGE
    """An identitifier for the value type."""

    data: str
    """The image data as base64-encoded string."""


class ArrayValueModel(BaseModel):
    """The model implementation for MLTE array values."""

    value_type: Literal[ValueType.ARRAY] = ValueType.ARRAY
    """An identitifier for the value type."""

    data: List[Any]
    """The array to capture."""


ValueModel.model_rebuild()


# Value type mapping to models.
VALUE_MODEL_CLASS: dict[
    ValueType,
    Union[
        type[IntegerValueModel],
        type[RealValueModel],
        type[OpaqueValueModel],
        type[ImageValueModel],
        type[ArrayValueModel],
    ],
] = {
    ValueType.INTEGER: IntegerValueModel,
    ValueType.REAL: RealValueModel,
    ValueType.OPAQUE: OpaqueValueModel,
    ValueType.IMAGE: ImageValueModel,
    ValueType.ARRAY: ArrayValueModel,
}


def get_model_class(type: ValueType):
    return VALUE_MODEL_CLASS[type]
