"""
mlte/session/state.py

Session state management for the MLTE library.
"""

from typing import Optional

from mlte.context import Context
from mlte.store.artifact.factory import create_store
from mlte.store.artifact.store import ArtifactStore


class Session:
    """
    The Session data structure encapsulates package-wide state.

    The primary function of the Session data structure is to provide
    convenient access to the MLTE context for application developers.
    """

    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super(Session, self).__new__(self)
        return self._instance

    def __init__(self):
        self._context: Optional[Context] = None
        """The MLTE context for the session."""

        self._store: Optional[ArtifactStore] = None
        """The MLTE store instance for the session."""

    @property
    def context(self) -> Context:
        if self._context is None:
            raise RuntimeError("Must initialize MLTE context for session.")
        return self._context

    @property
    def store(self) -> ArtifactStore:
        if self._store is None:
            raise RuntimeError("Must initialize MLTE store for session.")
        return self._store

    def _set_context(self, context: Context) -> None:
        """Set the session context."""
        self._context = context

    def _set_store(self, store: ArtifactStore) -> None:
        """Set the session store."""
        self._store = store


# Singleton session state
g_session = Session()


def session() -> Session:
    """Return the package global state."""
    return g_session


def set_context(namespace_id: str, model_id: str, version_id: str):
    """
    Set the global MLTE context.
    :param namespace_id: The namespace identifier
    :param model_id: The model identifier
    :param version_id: The version identifier
    """
    global g_session
    g_session._set_context(Context(namespace_id, model_id, version_id))


def set_store(artifact_store_uri: str):
    """
    Set the global MLTE context artifact store URI.
    :param artifact_store_uri: The artifact store URI string
    """
    global g_session
    g_session._set_store(create_store(artifact_store_uri))
