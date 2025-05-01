"""
mlte/artifact/type.py

MLTE artifact type implementation.

The artifact type enumeration is partitioned from the artifact model
implementation because it allows us to avoid a circular dependency amongst
the artifact base model, individual artifact models, and the type enum.
"""

from strenum import StrEnum


class ArtifactType(StrEnum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = "negotiation_card"
    """The negotiation card artifact type."""

    EVIDENCE = "evidence"
    """The evidence card artifact type."""

    TEST_SUITE = "test_suite"
    """The specification artifact type."""

    TEST_RESULTS = "test_results"
    """The results for a test suite artifact type."""

    REPORT = "report"
    """The report artifact type."""
