"""
mlte/spec/model.py

Model implementation for the Spec artifact.
"""

from typing import Any, Dict, List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.evidence.metadata import EvidenceMetadata
from mlte.model import BaseModel


class ConditionModel(BaseModel):
    """A description of a condition for a property."""

    name: str
    """A decriptive name for the condition, usually the method name used to call it."""

    arguments: List[Any] = []
    """The arguments used when validating the condition."""

    callback: str
    """A text-encoded, dilled-serialized version of the callback to execute when validating this condition."""


class ResultModel(BaseModel):
    """A description of a Result."""

    type: str
    """The type of result."""

    message: str
    """The message indicating the reason for status."""

    metadata: Optional[EvidenceMetadata]
    """Evidence metadata associated with the value."""


class PropertyModel(BaseModel):
    """A description of a property."""

    name: str
    """A name for the property."""

    description: Optional[str] = None
    """A general description of this property type."""

    rationale: Optional[str] = None
    """The rationale for this property being important in this situation."""

    conditions: Dict[str, ConditionModel] = {}
    """A dictionary of conditions, keyed by measurement id, to be validated for this property."""

    results: Dict[str, ResultModel] = {}
    """A dictionary of results, keyed by measurement id, which are only present when the conditions have been validated."""


class SpecModel(BaseModel):
    """The model implementation for the Spec artifact."""

    artifact_type: Literal[ArtifactType.SPEC]
    """Union discriminator."""

    properties: List[PropertyModel] = []
    """A list of properties for this spec."""


SpecModel.model_rebuild()
