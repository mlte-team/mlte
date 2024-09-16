"""
mlte/session/session.py

Session state management for the MLTE library.
"""

from typing import Optional

import mlte.store.artifact.util as storeutil
from mlte.context.context import Context
from mlte.store.artifact.factory import create_artifact_store
from mlte.store.artifact.store import ArtifactStore
from mlte.store.catalog.catalog_group import CatalogStoreGroup


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

        self._artifact_store: Optional[ArtifactStore] = None
        """The MLTE store instance for the session."""

        self._catalog_stores: CatalogStoreGroup = CatalogStoreGroup()
        """The list of catalog store instances maintained by the session object."""

    @property
    def context(self) -> Context:
        if self._context is None:
            raise RuntimeError("Must initialize MLTE context for session.")
        return self._context

    @property
    def artifact_store(self) -> ArtifactStore:
        if self._artifact_store is None:
            raise RuntimeError(
                "Must initialize MLTE artifact store for session."
            )
        return self._artifact_store

    def _set_context(self, context: Context) -> None:
        """Set the session context."""
        self._context = context

    def _set_artifact_store(self, artifact_store: ArtifactStore) -> None:
        """Set the session artifact store."""
        self._artifact_store = artifact_store

    def _add_catalog_store(self, store_uri: str, id: str):
        """Adds a catalog store."""
        self._catalog_stores.add_catalog_from_uri(id, store_uri)

    def create_context(self):
        """Creates the currently configured context in the currently configured session. Fails if either is not set. Does nothing if already created."""
        store = self.artifact_store
        context = self.context
        storeutil.create_parents(
            store.session(), context.model, context.version
        )


# Singleton session.
g_session = Session()


def session() -> Session:
    """Return the package global session."""
    return g_session


def set_context(model_id: str, version_id: str, lazy: bool = True):
    """
    Set the global MLTE context.
    :param model_id: The model identifier
    :param version_id: The version identifier
    :param lazy: Whether to wait to create the context until an artifact is written (True), or to eagerly create it immediately (False).
    """
    global g_session
    g_session._set_context(Context(model_id, version_id))
    if not lazy:
        g_session.create_context()


def set_store(artifact_store_uri: str):
    """
    Set the global MLTE context artifact store URI.
    :param artifact_store_uri: The artifact store URI string
    """
    global g_session
    g_session._set_artifact_store(create_artifact_store(artifact_store_uri))


def add_catalog_store(catalog_store_uri: str, id: str):
    """
    Adds a global MLTE catalog store URI.
    :param catalog_store_uri: The catalog store URI string
    """
    global g_session
    g_session._add_catalog_store(catalog_store_uri, id)