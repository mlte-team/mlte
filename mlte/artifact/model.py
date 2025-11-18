"""Model implementation for MLTE artifacts."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import ConfigDict, Field, model_validator
from strenum import StrEnum

from mlte.artifact.type import ArtifactType
from mlte.evidence.model import EvidenceModel
from mlte.model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.results.model import TestResultsModel
from mlte.store.query import Filterable
from mlte.tests.model import TestSuiteModel


class ArtifactLevel(StrEnum):
    """Level the artifact will exist at (model or version)."""

    MODEL = "model"
    """Store this artifact at the model level."""

    VERSION = "version"
    """Store this artifact at the version level."""


class ArtifactHeaderModel(BaseModel):
    """The ArtifactHeaderModel contains the common metadata for all artifacts."""

    identifier: str
    """The unique identifier for the artifact."""

    type: ArtifactType
    """The type identfier for the artifact."""

    timestamp: Optional[int] = -1
    """The timestamp of creation of this artifact, as Unix time."""

    creator: Optional[str] = None
    """The user that created this artifact."""

    level: ArtifactLevel = ArtifactLevel.VERSION
    """The level this artifact will exist at (model or version)."""

    model_config = ConfigDict(use_enum_values=True)


class ArtifactModel(Filterable):
    """The base model for all MLTE artifacts."""

    header: ArtifactHeaderModel
    """The artifact header."""

    body: Union[
        NegotiationCardModel,
        EvidenceModel,
        TestSuiteModel,
        TestResultsModel,
        ReportModel,
    ] = Field(..., discriminator="artifact_type")
    """The artifact body."""

    def get_identifier(self) -> str:
        return self.header.identifier

    def get_type(self) -> ArtifactType:
        return self.header.type

    @model_validator(mode="after")
    def post_validation_caller(self) -> ArtifactModel:
        """Called after validation, lets submodel do any needed post-processing."""
        self.body.post_validation_hook(self.header.identifier)
        return self
