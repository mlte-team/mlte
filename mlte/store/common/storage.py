"""
mlte/store/catalog/common/storage.py

Base storage class.
"""

from mlte.store.base import StoreURI


class Storage:
    def __init__(self, uri: StoreURI):
        self.uri = uri
        """The base URI."""

    def get_uri(self) -> StoreURI:
        """Get the base uri."""
        return self.uri

    def close(self):
        """Cleanup."""
        pass
