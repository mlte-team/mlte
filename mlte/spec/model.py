"""
mlte/spec/model.py

Model implementation for the Spec artifact.
"""

from typing import Dict, List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.model import BaseModel
from mlte.validation.model_condition import ConditionModel


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

    module: str
    """The full package and module path of the Property class."""


class SpecModel(BaseModel):
    """The model implementation for the Spec artifact."""

    artifact_type: Literal[ArtifactType.SPEC] = ArtifactType.SPEC
    """Union discriminator."""

    properties: List[PropertyModel] = []
    """A list of properties for this spec."""


SpecModel.model_rebuild()
