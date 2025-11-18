"""MLTE catalog store interface implementation."""

from __future__ import annotations

from mlte.store.base import Store
from mlte.store.catalog.store_session import CatalogStoreSession


class CatalogStore(Store):
    read_only: bool = False
    """Whether this catalog is read only or not."""

    def session(self) -> CatalogStoreSession:
        """Return a session handle for a catalog store session instance."""
        raise NotImplementedError("Can't call session on a base Store.")
