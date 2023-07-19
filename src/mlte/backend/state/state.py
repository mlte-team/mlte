"""
store/state/state.py

Globally-accessible application state.
"""

from typing import Optional
from mlte.store.backend import BackendEngine


class State:
    """Global state object."""

    def __init__(self):
        self._engine: Optional[BackendEngine] = None

    def set_engine(self, engine: BackendEngine):
        """Set the globally-configured backend engine."""
        self._engine = engine

    @property
    def engine(self) -> BackendEngine:
        """Get the globally-configured backend engine."""
        if self._engine is None:
            raise RuntimeError("Engine is not configured.")
        return self._engine


# Globally-accessible application state
state = State()
