"""
mlte/spec/model.py

Model implementation for the Spec artifact.
"""

from typing import Optional, List, Literal, Any

from mlte.artifact.type import ArtifactType
from mlte.model import BaseModel


class ConditionModel(BaseModel):
    """A description of a condition for a property."""

    name: Optional[str] = None
    """A decriptive name for the condition, usually the method name used to call it."""

    arguments: List[Any] = []
    """The arguments used when validating the condition."""

    callback: Optional[str] = None
    """A text-encoded, dilled-serialized version of the callback to execute when validating this condition."""


class PropertyModel(BaseModel):
    """A description of a property."""

    name: Optional[str] = None
    """A name for the property."""

    repr: Optional[str] = None
    """A string representation of the object."""

    description: Optional[str] = None
    """A general description of this property type."""

    rationale: Optional[str] = None
    """The rationale for this property being important in this situation."""

    conditions: List[ConditionModel] = []
    """A list of conditions to be validated for this property."""


class SpecModel(BaseModel):
    """The model implementation for the Spec artifact."""

    artifact_type: Literal[ArtifactType.SPEC]
    """Union discriminator."""

    properties: List[PropertyModel] = []
    """A list of properties for this spec."""


SpecModel.model_rebuild()
