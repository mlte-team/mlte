"""
mlte/artifact/type.py

Definition of enumeration for MLTE artifact types.

NOTE: It is important that we keep this definition separate from the
definition of Artifact itself. Artifact contains runtime dependencies
on things like the global session. Meanwhile, storage models for
artifacts depend on this enumeration. If these two worlds are allowed
to "meet", we have an inevitable circular import error. The partition
here is critical to ensure that we keep these worlds separate.
"""

from enum import Enum


class ArtifactType(str, Enum):
    """Enumerates all supported artifact types."""

    NEGOTIATION_CARD = "negotiation_card"
    """The negotiation card artifact type."""
