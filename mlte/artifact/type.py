"""
mlte/artifact/type.py

MLTE artifact type implementation.

The artifact type enumeration is partitioned from the artifact model
implementation because it allows us to avoid a circular dependency amongst
the artifact base model, individual artifact models, and the type enum.
"""

from enum import Enum, auto


class ArtifactType(str, Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = auto()
    """The negotiation card artifact type."""

    VALUE = auto()
    """The value card artifact type."""
