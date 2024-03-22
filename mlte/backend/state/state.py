"""
mlte/backend/state/state.py

Globally-accessible application state.
"""

from typing import Optional

from mlte.store.artifact.store import ArtifactStore
from mlte.store.user.store import UserStore


class State:
    """Global state object."""

    def __init__(self):
        self._artifact_store: Optional[ArtifactStore] = None
        """The artifact store instance maintained by the state object."""

        self._user_store: Optional[UserStore] = None
        """The user store instance maintained by the state object."""

    def set_artifact_store(self, store: ArtifactStore):
        """Set the globally-configured backend artifact store."""
        self._artifact_store = store

    def set_user_store(self, store: UserStore):
        """Set the globally-configured backend artifact store."""
        self._user_store = store

    @property
    def artifact_store(self) -> ArtifactStore:
        """Get the globally-configured backend artifact store."""
        if self._artifact_store is None:
            raise RuntimeError("Artifact store is not configured.")
        return self._artifact_store

    @property
    def user_store(self) -> UserStore:
        """Get the globally-configured backend user store."""
        if self._user_store is None:
            raise RuntimeError("User store is not configured.")
        return self._user_store


# Globally-accessible application state
state = State()
