"""
mlte/spec/model.py

Model implementation for the Spec artifact.
"""

from typing import Dict, List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.model import BaseModel
from mlte.validation.model_condition import ConditionModel


class QACategoryModel(BaseModel):
    """A description of a quality attribute category."""

    name: str
    """A name for the QACategory."""

    description: Optional[str] = None
    """A general description of this QACategory type."""

    rationale: Optional[str] = None
    """The rationale for this QACategory being important in this situation."""

    conditions: Dict[str, ConditionModel] = {}
    """A dictionary of conditions, keyed by measurement id, to be validated for this QACategory."""

    module: str
    """The full package and module path of the QACategory class."""


class SpecModel(BaseModel):
    """The model implementation for the Spec artifact."""

    artifact_type: Literal[ArtifactType.SPEC] = ArtifactType.SPEC
    """Union discriminator."""

    qa_categories: List[QACategoryModel] = []
    """A list of QACategory for this spec."""


SpecModel.model_rebuild()
