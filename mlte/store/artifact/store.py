"""MLTE artifact store interface implementation."""

from __future__ import annotations

from mlte.store.artifact.store_session import ArtifactStoreSession
from mlte.store.base import Store


class ArtifactStore(Store):
    """
    An abstract artifact store.

    A Store instance is the "static" part of a store configuration.
    In contrast, a StoreSession represents an active session with the store.
    """

    def session(self) -> ArtifactStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Can't call session on a base Store.")
