"""
Implementation of HTTP catalog store group.
"""

from __future__ import annotations

from typing import Any, List, Optional, OrderedDict, Tuple

from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog.store import (
    CatalogEntryMapper,
    CatalogStore,
    CatalogStoreSession,
)
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpStorage
from mlte.user.model import MethodType, ResourceType

ENTRY_URL_KEY = "entry"


# -----------------------------------------------------------------------------
# HttpCatalogGroupStore
# -----------------------------------------------------------------------------


class HttpCatalogGroupStore(CatalogStore):
    """
    A HTTP implementation of the MLTE catalog store group. Note that it is slightly
    different than the other implementations, in mapping to a store group through a
    backend, instead of a simple catalog store.
    """

    def __init__(
        self, *, uri: StoreURI, client: Optional[OAuthHttpClient] = None
    ) -> None:
        super().__init__(uri=uri)

        self.storage = HttpStorage(
            uri=uri, resource_type=ResourceType.CATALOG, client=client
        )
        """HTTP storage."""

    def session(self) -> CatalogStoreSession:
        """
        Return a session handle for the store instance.
        :return: The session handle
        """
        return HttpCatalogGroupStoreSession(
            storage=self.storage, read_only=self.read_only
        )


# -----------------------------------------------------------------------------
# HttpCatalogGroupStoreSession
# -----------------------------------------------------------------------------


class HttpCatalogGroupStoreSession(CatalogStoreSession):
    """An HTTP implementation of the MLTE catalog store session."""

    def __init__(
        self, *, storage: HttpStorage, read_only: bool = False
    ) -> None:
        self.storage = storage
        """Http Storage"""

        self.read_only = read_only
        """Whether this is read only or not."""

        self.entry_mapper = HTTPCatalogGroupEntryMapper(storage=self.storage)
        """The mapper to entries CRUD."""

        storage.start_session()

    def close(self):
        # No closing needed.
        pass


# -----------------------------------------------------------------------------
# HTTPCatalogGroupEntryMapper
# -----------------------------------------------------------------------------


class HTTPCatalogGroupEntryMapper(CatalogEntryMapper):
    """HTTP mapper for the catalog group entry resource."""

    COMPOSITE_ID_SEPARATOR = "--"

    def __init__(self, storage: HttpStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(self, entry: CatalogEntry, context: Any = None) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        local_catalog_id, _ = self.split_ids(entry.header.identifier)
        new_entry = self._convert_to_local(entry)

        response = self.storage.post(
            json=new_entry.to_json(), groups=_entry_group(local_catalog_id)
        )

        local_entry = CatalogEntry(**response)
        return self._convert_to_remote(local_entry)

    def edit(self, entry: CatalogEntry, context: Any = None) -> CatalogEntry:
        # Entry id contains the remote catalog id as well.
        local_catalog_id, _ = self.split_ids(entry.header.identifier)
        edited_entry = self._convert_to_local(entry)

        response = self.storage.put(
            json=edited_entry.to_json(), groups=_entry_group(local_catalog_id)
        )

        local_entry = CatalogEntry(**response)
        return self._convert_to_remote(local_entry)

    def read(
        self, catalog_and_entry_id: str, context: Any = None
    ) -> CatalogEntry:
        catalog_id, entry_id = self.split_ids(catalog_and_entry_id)
        response = self.storage.get(
            id=entry_id, groups=_entry_group(catalog_id)
        )

        local_entry = CatalogEntry(**response)
        return self._convert_to_remote(local_entry)

    def list(self, context: Any = None) -> List[str]:
        entries = self.list_details()
        return [entry.header.identifier for entry in entries]

    def delete(
        self, catalog_and_entry_id: str, context: Any = None
    ) -> CatalogEntry:
        local_catalog_id, entry_id = self.split_ids(catalog_and_entry_id)

        response = self.storage.delete(
            id=entry_id, groups=_entry_group(local_catalog_id)
        )

        local_entry = CatalogEntry(**response)
        return self._convert_to_remote(local_entry)

    def list_details(
        self,
        context: Any = None,
        limit: int = CatalogEntryMapper.DEFAULT_LIST_LIMIT,
        offset: int = 0,
    ) -> List[CatalogEntry]:
        # This is a bit hacky, in that we have a pseudo resource type "catalogs",
        # and a pseudo resource id "entry" to get all details of all entries.
        response = self.storage.send_command(
            MethodType.GET,
            id="entry",
            resource_type=f"{ResourceType.CATALOG.value}s",
        )
        return [
            self._convert_to_remote(CatalogEntry(**entry)) for entry in response
        ][offset : offset + limit]

    @staticmethod
    def split_ids(composite_id: Optional[str]) -> Tuple[str, str]:
        if not composite_id:
            raise RuntimeError("No composite id received")

        parts = composite_id.split(
            HTTPCatalogGroupEntryMapper.COMPOSITE_ID_SEPARATOR
        )
        if len(parts) != 2:
            raise RuntimeError(f"Invalid composite id provided: {composite_id}")
        return parts[0], parts[1]

    @staticmethod
    def generate_composite_id(id1: Optional[str], id2: str) -> str:
        """Creates a composite id given two ids."""
        if id1:
            return f"{id1}{HTTPCatalogGroupEntryMapper.COMPOSITE_ID_SEPARATOR}{id2}"
        else:
            return id2

    def _convert_to_local(self, entry: CatalogEntry) -> CatalogEntry:
        """Creates a new entry from the given one, converting it to local by moving the remote catalog id from its identifier."""
        new_entry = entry.model_copy()
        new_entry.header = entry.header.model_copy()

        local_catalog_id, entry_id = self.split_ids(entry.header.identifier)
        http_catalog_id = new_entry.header.catalog_id
        new_entry.header.identifier = entry_id
        new_entry.header.catalog_id = self.generate_composite_id(
            http_catalog_id, local_catalog_id
        )

        return new_entry

    def _convert_to_remote(self, entry: CatalogEntry) -> CatalogEntry:
        """Creates a new entry from the given one, convertint it to remote by moving the remote catalog id to its identifier."""
        new_entry = entry.model_copy()
        new_entry.header = entry.header.model_copy()

        http_catalog_id, local_catalog_id = self.split_ids(
            new_entry.header.catalog_id
        )
        entry_id = new_entry.header.identifier
        new_entry.header.identifier = self.generate_composite_id(
            local_catalog_id, entry_id
        )
        new_entry.header.catalog_id = http_catalog_id

        return new_entry


def _entry_group(catalog_id: str) -> OrderedDict[str, str]:
    """Returns the resource group info for entries inside a catalog."""
    return OrderedDict([(catalog_id, ENTRY_URL_KEY)])
