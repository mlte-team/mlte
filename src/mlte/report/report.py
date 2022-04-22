"""
A model test report.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

class ReportAttribute:
    """The base class for report attributes."""

    def to_json():
        pass

    def from_json():
        pass

@dataclass
class ReportMetadata(ReportAttribute):
    """Metadata for the report."""

    authors: List[str] = field(default_factory=list)
    """The authors of the report."""

    timestamp: Optional[int] = None
    """The time at which the report was generated."""

    source_url: Optional[str] = None
    """The URL for model source."""

    artifacts_url: Optional[str] = None
    """The URL for model artifacts."""

@dataclass
class ModelOverview(ReportAttribute):
    """The model overview field of the report."""
    
    text: Optional[str] = None
    """The text that appears in the ModelOverview field."""

@dataclass
class Report(ReportAttribute):
    """The top-level model test report."""

    report_metadata: ReportMetadata = field(default_factory=ReportMetadata)
    """The report metadata."""

    model