"""
mlte/web/store/state/state.py

Globally-accessible application state.
"""

from typing import Optional

from mlte.store.artifact.store import ArtifactStore


class State:
    """Global state object."""

    def __init__(self):
        self._store: Optional[ArtifactStore] = None
        """The store instance maintained by the state object."""

    def set_store(self, store: ArtifactStore):
        """Set the globally-configured backend store."""
        self._store = store

    @property
    def store(self) -> ArtifactStore:
        """Get the globally-configured backend store."""
        if self._store is None:
            raise RuntimeError("Store is not configured.")
        return self._store


# Globally-accessible application state
state = State()
