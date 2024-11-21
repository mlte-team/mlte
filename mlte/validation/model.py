"""
mlte/validation/model.py

Model implementation for the ValidatedSpec artifact.
"""

from typing import Dict, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel
from mlte.spec.model import SpecModel


class ResultModel(BaseModel):
    """A description of a Result."""

    type: str
    """The type of result."""

    message: str
    """The message indicating the reason for status."""

    metadata: Optional[EvidenceMetadata]
    """Evidence metadata associated with the value."""


class ValidatorModel(BaseModel):
    """A description of a validator for a test."""

    bool_exp: Optional[str]
    """A text-encoded, dilled-serialized version of the callback to execute when checking the bool condition."""

    success: str
    """A string to be used when recording that the validation was succesful."""

    failure: str
    """A string to be used when recording that the validation was not succesful."""

    ignore: str
    """A string to be used when recording that the validation was not checked against a condition, just recorded information."""


class ValidatedSpecModel(BaseModel):
    """The model implementation for the ValidatedSpec artifact."""

    artifact_type: Literal[
        ArtifactType.VALIDATED_SPEC
    ] = ArtifactType.VALIDATED_SPEC

    """Union discriminator."""

    spec_identifier: str = ""
    """The identifier of the Spec this ValidatedSpec came from."""

    spec: Optional[SpecModel] = None
    """A link to the actual Spec details."""

    results: Dict[str, Dict[str, ResultModel]] = {}
    """A list of validation results, for each measurement id, grouped by property."""


ValidatedSpecModel.model_rebuild()
