"""Validator for the tags field of a catalog entry."""

from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.validators.cross_validator import CrossValidator


class CatalogTagValidator(CrossValidator):
    """Implementation of CrossValidator to validate a catalog entries tags against custom list store."""

    def __init__(
        self,
        custom_list_store: CustomListStore,
    ):
        """
        Initialize a CatalogTagValidator instance.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.custom_list_store = custom_list_store

    def validate(self, new_entry: CatalogEntry) -> None:
        with ManagedCustomListSession(
            self.custom_list_store.session()
        ) as session:
            for tag in new_entry.tags:
                try:
                    session.custom_list_entry_mapper.read(
                        tag,
                        CustomListName.TAGS,
                    )
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog entry tag validation failure. Tag: {tag} not found. For catalog entry {new_entry.header.identifier}."
                    )
