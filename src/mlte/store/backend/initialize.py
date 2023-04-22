"""
store/backend/initialize.py

Initialize the backend. This is the second
step in the backend initialization lifecyle.
"""

from mlte.store.backend.engine import g_engine


def initialize_engine() -> None:
    """Initialize the engine for use."""
    g_engine.initialize()
