"""Implementation of HTTP custom list store"""

import typing
from typing import Optional, OrderedDict

from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.store.base import StoreURI
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpStorage
from mlte.store.custom_list.store import CustomListStore
from mlte.store.custom_list.store_session import (
    CustomListEntryMapper,
    CustomListStoreSession,
)
from mlte.user.model import ResourceType

ENTRY_URL_KEY = "entry"


# -----------------------------------------------------------------------------
# HttpCustomListStore
# -----------------------------------------------------------------------------


class HttpCustomListStore(CustomListStore):
    """A http implementation of the MLTE custom list store."""

    def __init__(
        self, *, uri: StoreURI, client: Optional[OAuthHttpClient] = None
    ) -> None:
        super().__init__(uri=uri)

        self.storage = HttpStorage(
            uri=uri, resource_type=ResourceType.CUSTOM_LIST, client=client
        )
        """HTTP storage."""

    def session(self) -> CustomListStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCustomListStoreSession(storage=self.storage)


# -----------------------------------------------------------------------------
# HttpCustomListStoreSession
# -----------------------------------------------------------------------------


class HttpCustomListStoreSession(CustomListStoreSession):
    """An HTTP implementation of the MLTE custom list store session."""

    def __init__(self, *, storage: HttpStorage) -> None:
        self.storage = storage
        """HTTP storage."""

        self.custom_list_entry_mapper = HttpCustomListEntryMapper(storage)

    def close(self):
        # No closing needed
        pass


# -----------------------------------------------------------------------------
# HttpCustomListEntryMapper
# -----------------------------------------------------------------------------


class HttpCustomListEntryMapper(CustomListEntryMapper):
    """HTTP mapper for the custom list resource."""

    def __init__(self, storage: HttpStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(
        self,
        new_entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        list_name = self._check_valid_custom_list(list_name)
        response = self.storage.post(
            json=new_entry.to_json(), groups=_list_group(list_name)
        )
        return CustomListEntryModel(**response)

    def read(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        list_name = self._check_valid_custom_list(list_name)
        response = self.storage.get(
            id=entry_name, groups=_list_group(list_name)
        )
        return CustomListEntryModel(**response)

    def list(self, list_name: Optional[CustomListName] = None) -> list[str]:
        list_name = self._check_valid_custom_list(list_name)
        response = self.storage.get()
        return typing.cast(list[str], response)

    def edit(
        self,
        updated_entry: CustomListEntryModel,
        list_name: Optional[CustomListName] = None,
    ) -> CustomListEntryModel:
        list_name = self._check_valid_custom_list(list_name)
        response = self.storage.put(
            json=updated_entry.to_json(), groups=_list_group(list_name)
        )
        return CustomListEntryModel(**response)

    def delete(
        self, entry_name: str, list_name: Optional[CustomListName] = None
    ) -> CustomListEntryModel:
        list_name = self._check_valid_custom_list(list_name)
        response = self.storage.delete(
            id=entry_name, groups=_list_group(list_name)
        )
        return CustomListEntryModel(**response)


def _list_group(list_name: str) -> OrderedDict[str, str]:
    """Returns the resource group info for custom list."""
    return OrderedDict([(list_name, ENTRY_URL_KEY)])
