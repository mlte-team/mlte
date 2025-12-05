"""Validator for the user field of a catalog entry."""

from mlte.catalog.model import CatalogEntry
from mlte.store.error import ErrorNotFound
from mlte.store.user.store import UserStore
from mlte.store.user.store_session import ManagedUserSession
from mlte.store.validators.cross_validator import CrossValidator


class CatalogUserValidator(CrossValidator):
    """Implementation of CrossValidator to validate an catalog entry against the user store."""

    def __init__(
        self,
        user_store: UserStore,
    ):
        """
        Initialize a CatalogUserValidator instance.
        :param user_store: User store to use for validation.
        """
        self.user_store = user_store

    def validate(self, new_entry: CatalogEntry) -> None:
        with ManagedUserSession(self.user_store.session()) as session:
            if new_entry.header.creator is not None:
                try:
                    session.user_mapper.read(new_entry.header.creator)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog creator validation failure. Creator user: {new_entry.header.creator} not found. For catalog entry {new_entry.header.identifier}."
                    )

            if new_entry.header.updater is not None:
                try:
                    session.user_mapper.read(new_entry.header.updater)
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog creator validation failure. Updater user: {new_entry.header.updater} not found. For catalog entry {new_entry.header.identifier}."
                    )
