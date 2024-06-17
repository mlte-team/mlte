"""
mlte/artifact/model.py

Model implementation for MLTE artifacts.
"""

from typing import Optional, Union

from pydantic import ConfigDict, Field

from mlte.artifact.type import ArtifactType
from mlte.model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.spec.model import SpecModel
from mlte.validation.model import ValidatedSpecModel
from mlte.value.model import ValueModel


class ArtifactHeaderModel(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the artifact."""

    type: ArtifactType
    """The type identfier for the artifact."""

    timestamp: Optional[int] = -1
    """The timestamp of creation of this artifact, as Unix time."""

    creator: Optional[str]
    """The user that created this artifact."""

    model_config = ConfigDict(use_enum_values=True)


class ArtifactModel(BaseModel):
    """The base model for all MLTE artifacts."""

    header: ArtifactHeaderModel
    """The artifact header."""

    body: Union[
        NegotiationCardModel,
        ValueModel,
        SpecModel,
        ValidatedSpecModel,
        ReportModel,
    ] = Field(..., discriminator="artifact_type")
    """The artifact body."""
