"""
mlte/spec/model.py

Model implementation for the Spec artifact.
"""

from typing import Dict, List, Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.measurement.model import MeasurementModel
from mlte.model import BaseModel
from mlte.validation.model_condition import ConditionModel, ValidatorModel


class TestCaseModel(BaseModel):
    name: str
    """A name/id for the test case."""

    goal: str
    """A description of the goal of this test case."""

    qas_list: list[str] = []
    """A list of ids of Qualit Attribute Scenarios that this case is addressing."""

    measurement: Optional[MeasurementModel] = None
    """Measurement to be used with this test case."""

    validator: Optional[ValidatorModel] = None
    """Validation to be used for this test case."""


class TestSuiteModel(BaseModel):
    """The model implementation for the TestSuite artifact."""

    artifact_type: Literal[ArtifactType.SPEC] = ArtifactType.SPEC
    """Union discriminator."""

    test_cases: List[TestCaseModel] = []


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
