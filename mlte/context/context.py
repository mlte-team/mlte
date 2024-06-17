"""
mlte/context/context.py

MLTE artifact context definition.

The MLTE artifact context defines the information necessary to
utilize the MLTE package to generate, persist, and load
MLTE evaluation artifacts.
"""

from dataclasses import dataclass


@dataclass
class Context:
    """
    The MLTE context establishes the artifact context for a MLTE evaluation session.
    """

    model: str
    """The context model identifier."""

    version: str
    """The context model version identifier."""
