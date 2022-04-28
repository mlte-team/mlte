"""
A model test report.

Acknowledgements:
    The contents of a mlte model report, and the
    implementation of model report generation
    in this file is adapted from the work by the
    TensorFlow team in the Model Card Toolkit:
    https://github.com/tensorflow/model-card-toolkit
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from ..suites import SuiteReport
from ..internal.schema import REPORT_LATEST_SCHEMA_VERSION


class ReportAttribute:
    """The base class for report attributes."""

    def to_json(self) -> Dict[str, Any]:
        """
        Convert a ReportAttribute instance to a JSON document.

        :return: The converted document
        :rtype: Dict[str, Any]
        """
        return dataclasses.asdict(
            self,
            dict_factory=lambda properties: {k: v for k, v in properties if v},
        )


# -----------------------------------------------------------------------------
# Report Sub-Sections
# -----------------------------------------------------------------------------


@dataclass
class Dataset(ReportAttribute):
    """A description of a dataset used to train the model."""

    name: Optional[str] = None
    """An identifier for the dataset."""

    link: Optional[str] = None
    """A method to access the dataset."""

    description: Optional[str] = None
    """A description of the dataset."""


@dataclass
class User(ReportAttribute):
    """A description of an intended user of the model."""

    description: Optional[str] = None
    """A description of the intended user."""


@dataclass
class UseCase(ReportAttribute):
    """A description of an intended use case of the model."""

    description: Optional[str] = None
    """A description of the use case."""


@dataclass
class Limitation(ReportAttribute):
    """A description of a technical limitation of the model."""

    description: Optional[str] = None
    """A description of the limitation."""


# -----------------------------------------------------------------------------
# Report Sections
# -----------------------------------------------------------------------------


@dataclass
class Metadata(ReportAttribute):
    """Metadata for the report."""

    project_name: Optional[str] = None
    """The name of the project."""

    authors: List[str] = field(default_factory=list)
    """The authors of the report."""

    source_url: Optional[str] = None
    """The URL for model source."""

    artifacts_url: Optional[str] = None
    """The URL for model artifacts."""

    timestamp: Optional[str] = None
    """The time at which the report was generated."""


@dataclass
class ModelDetails(ReportAttribute):
    """The `model details` section of the report."""

    name: Optional[str] = None
    """The name of the model."""

    overview: Optional[str] = None
    """A brief overview of the model."""

    documentation: Optional[str] = None
    """A detailed description of the model."""


@dataclass
class ModelSpecification(ReportAttribute):
    """The `model specification` section of the report."""

    domain: Optional[str] = None
    """The domain of the model."""

    architecture: Optional[str] = None
    """A description of the model architecture."""

    input: Optional[str] = None
    """A description of model inputs."""

    output: Optional[str] = None
    """A description of model outputs."""

    data: List[Dataset] = field(default_factory=list)
    """A description of the data used to train the model."""


@dataclass
class Considerations(ReportAttribute):
    """The `considerations` section of the report."""

    users: List[User] = field(default_factory=list)
    """A description of the intended users of the model."""

    use_cases: List[UseCase] = field(default_factory=list)
    """A description of the intended use cases for the model."""

    limitations: List[Limitation] = field(default_factory=list)
    """A description of the technical limitations of the model."""


@dataclass
class Report(ReportAttribute):
    """The top-level model test report."""

    metadata: Metadata = field(default_factory=Metadata)
    """The report metadata."""

    model_details: ModelDetails = field(default_factory=ModelDetails)
    """The model details."""

    model_specification: ModelSpecification = field(
        default_factory=ModelSpecification
    )
    """The model specification."""

    considerations: Considerations = field(default_factory=Considerations)
    """Model considerations."""

    suite: SuiteReport = field(default_factory=lambda: SuiteReport({}))
    """The model test suite report."""

    def json(self) -> Dict[str, Any]:
        """
        Convert a ReportAttribute instance to a JSON document.

        :return: The converted document
        :rtype: Dict[str, Any]
        """
        document = dataclasses.asdict(
            self,
            dict_factory=lambda properties: {k: v for k, v in properties if v},
        )
        # Manually serialize the suite-level document
        document["suite"] = self.suite.document
        # Manually insert the schema version
        document["schema_version"] = REPORT_LATEST_SCHEMA_VERSION
        return document
