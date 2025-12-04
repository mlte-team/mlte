"""Validator for the quality attribute fields of a catalog entry."""

from mlte.catalog.model import CatalogEntry
from mlte.custom_list.custom_list_names import CustomListName
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import ManagedCustomListSession
from mlte.store.error import ErrorNotFound
from mlte.store.validators.cross_validator import CrossValidator


class CatalogQAValidator(CrossValidator):
    """Implementation of CrossValidator to validate a catalog entry QA ßagainst custom list store."""

    def __init__(
        self,
        custom_list_store: CustomListStore,
    ):
        """
        Initialize a CatalogQAValidator instance.
        :param custom_list_store: Custom list store store to use for validation.
        """
        self.custom_list_store = custom_list_store

    def validate(self, new_entry: CatalogEntry) -> None:
        if new_entry.quality_attribute != "":
            with ManagedCustomListSession(
                self.custom_list_store.session()
            ) as session:
                try:
                    session.custom_list_entry_mapper.read(
                        new_entry.quality_attribute,
                        CustomListName.QUALITY_ATTRIBUTES,
                    )
                except ErrorNotFound:
                    raise RuntimeError(
                        f"Catalog entry quality attribute validation failure. Custom list entry: {new_entry.quality_attribute} not found. For catalog entry {new_entry.header.identifier}."
                    )
