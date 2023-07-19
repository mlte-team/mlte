"""
mlte/store/underlying/memory.py

Implementation of in-memory artifact store.
"""

from mlte.store.store import Store, StoreSession, StoreURI


class InMemoryStoreSession(StoreSession):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self) -> None:
        pass


class InMemoryStore(Store):
    """An in-memory implementation of the MLTE artifact store."""

    def __init__(self, uri: StoreURI) -> None:
        super().__init__(uri=uri)

    def session(self) -> InMemoryStoreSession:  # type: ignore[override]
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
