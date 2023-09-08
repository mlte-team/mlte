"""
mlte/validation/model.py

Model implementation for the ValidatedSpec artifact.
"""

from typing import Dict, List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel
from mlte.spec.model import PropertyModel


class ResultModel(BaseModel):
    """A description of a Result."""

    type: str
    """The type of result."""

    message: str
    """The message indicating the reason for status."""

    metadata: Optional[EvidenceMetadata]
    """Evidence metadata associated with the value."""


class PropertyAndResultsModel(PropertyModel):
    """A description of a property, along with results."""

    results: Dict[str, ResultModel] = {}
    """A dictionary of results, keyed by measurement id, which are only present when the conditions have been validated."""


class ValidatedSpecModel(BaseModel):
    """The model implementation for the ValidatedSpec artifact."""

    artifact_type: Literal[ArtifactType.VALIDATED_SPEC]
    """Union discriminator."""

    spec_identifier: str = ""
    """The identifier of the Spec this ValidatedSpec came from."""

    properties: List[PropertyAndResultsModel] = []
    """A list of properties for this spec, along with validation results."""


ValidatedSpecModel.model_rebuild()
