"""
Model implementation for MLTE evidence.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Union

from pydantic import Field
from strenum import StrEnum

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel


class EvidenceType(StrEnum):
    """An ennumeration over supported evidence types."""

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

    STRING = "string"
    """A string media type."""


class EvidenceModel(BaseModel):
    """The model implementation for MLTE evidence."""

    artifact_type: Literal[ArtifactType.EVIDENCE] = ArtifactType.EVIDENCE
    """Union discriminator."""

    metadata: EvidenceMetadata
    """Evidence information (id and measurement it came from)."""

    evidence_class: str
    """Full path to class that implements this evidence."""

    value: Union[
        "IntegerValueModel",
        "RealValueModel",
        "OpaqueValueModel",
        "ImageValueModel",
        "ArrayValueModel",
        "StringValueModel",
    ] = Field(..., discriminator="evidence_type")
    """The body of the evidence."""


class IntegerValueModel(BaseModel):
    """The model implementation for MLTE integer values."""

    evidence_type: Literal[EvidenceType.INTEGER] = EvidenceType.INTEGER
    """An identitifier for the evidence type."""

    integer: int
    """The encapsulated value."""


class RealValueModel(BaseModel):
    """The model implementation for MLTE real values."""

    evidence_type: Literal[EvidenceType.REAL] = EvidenceType.REAL
    """An identitifier for the evidence type."""

    real: float
    """The encapsulated value."""


class OpaqueValueModel(BaseModel):
    """The model implementation for MLTE opaque values."""

    evidence_type: Literal[EvidenceType.OPAQUE] = EvidenceType.OPAQUE
    """An identitifier for the evidence type."""

    data: Dict[str, Any]
    """Encapsulated, opaque data."""


class ImageValueModel(BaseModel):
    """The model implementation for MLTE image values."""

    evidence_type: Literal[EvidenceType.IMAGE] = EvidenceType.IMAGE
    """An identitifier for the evidence type."""

    data: str
    """The image data as base64-encoded string."""


class ArrayValueModel(BaseModel):
    """The model implementation for MLTE array values."""

    evidence_type: Literal[EvidenceType.ARRAY] = EvidenceType.ARRAY
    """An identitifier for the evidence type."""

    data: List[Any]
    """The array to capture."""


class StringValueModel(BaseModel):
    """The model implementation for MLTE string values."""

    evidence_type: Literal[EvidenceType.STRING] = EvidenceType.STRING
    """An identitifier for the evidence type."""

    string: str
    """The encapsulated string."""


# Value type mapping to models.
EVIDENCE_MODEL_CLASS: dict[
    EvidenceType,
    Union[
        type[IntegerValueModel],
        type[RealValueModel],
        type[OpaqueValueModel],
        type[ImageValueModel],
        type[ArrayValueModel],
    ],
] = {
    EvidenceType.INTEGER: IntegerValueModel,
    EvidenceType.REAL: RealValueModel,
    EvidenceType.OPAQUE: OpaqueValueModel,
    EvidenceType.IMAGE: ImageValueModel,
    EvidenceType.ARRAY: ArrayValueModel,
}


def get_model_class(type: EvidenceType):
    return EVIDENCE_MODEL_CLASS[type]
