"""
mlte/artifact/model.py

Model implementation for MLTE artifacts.
"""

from typing import Any, Optional, Union

from pydantic import ConfigDict, Field

from mlte.artifact.type import ArtifactType
from mlte.evidence.model import EvidenceModel
from mlte.model import BaseModel
from mlte.negotiation.model import NegotiationCardModel
from mlte.report.model import ReportModel
from mlte.spec.model import TestSuiteModel
from mlte.store.query import Filterable
from mlte.validation.model import TestResultsModel


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
        TestSuiteModel,
    ] = Field(..., discriminator="artifact_type")
    """The artifact body."""

    def get_identifier(self) -> str:
        return self.header.identifier

    def get_type(self) -> Any:
        return self.header.type
