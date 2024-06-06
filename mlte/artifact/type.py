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

    VALUE = "value"
    """The value card artifact type."""

    SPEC = "spec"
    """The specification artifact type."""

    VALIDATED_SPEC = "validated_spec"
    """The validated specification artifact type."""

    REPORT = "report"
    """The report artifact type."""
