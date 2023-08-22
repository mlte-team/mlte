"""
mlte/context/context.py

MLTE session context definition.

The MLTE context defines the information necessary to
utilize the MLTE package to generate, persist, and load
MLTE evaluation artifacts.
"""

from dataclasses import dataclass


@dataclass
class Context:
    """
    The MLTE context establishes the context for a MLTE evaluation session.

    NOTE(Kyle): Previously, this module had an explicit dependency on global
    library state. This made testing difficult in that we had to establish the
    global MLTE context through the usual hooks (those that developers use in
    their applications). I have since refactored this to ensure that the Context
    is a standalone data structure that is then exported by the global state module.
    """

    namespace: str
    """The context namespace."""

    model: str
    """The context model identifier."""

    version: str
    """The context model version identifier."""
