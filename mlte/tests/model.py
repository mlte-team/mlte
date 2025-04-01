"""
Model implementation for the TestSuite artifact.
"""

from typing import Literal, Optional

from mlte.artifact.type import ArtifactType
from mlte.measurement.model import MeasurementMetadata
from mlte.model import BaseModel
from mlte.validation.model import ValidatorModel


class TestCaseModel(BaseModel):
    identifier: str
    """A name/id for the test case."""

    goal: str
    """A description of the goal of this test case."""

    qas_list: list[str] = []
    """A list of ids of Quality Attribute Scenarios that this case is addressing."""

    measurement: Optional[MeasurementMetadata] = None
    """Measurement to be used with this test case."""

    validator: Optional[ValidatorModel] = None
    """Validation to be used for this test case."""


class TestSuiteModel(BaseModel):
    """The model implementation for the TestSuite artifact."""

    artifact_type: Literal[ArtifactType.TEST_SUITE] = ArtifactType.TEST_SUITE
    """Union discriminator."""

    test_cases: list[TestCaseModel] = []
