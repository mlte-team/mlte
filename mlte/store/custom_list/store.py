"""
mlte/store/custom_list/store.py

MLTE custom list store implementation
"""

from __future__ import annotations

from mlte.store.base import Store, StoreSession

# -----------------------------------------------------------------------------
# CustomListStore
# -----------------------------------------------------------------------------


class CustomListStore(Store):
    """
    An abstract custom list store
    """

    def __init__(self, uri: StoreURI):
        """Base constructor"""
        super().__init__(uri=uri)
        """Store uri."""

    def session(self) -> CustomListStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        raise NotImplementedError("Cannot get handle to abstract Store.")
