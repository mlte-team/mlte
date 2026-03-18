"""
Implementation of HTTP catalog store group.

NOTE: indicating the remote catalog that an entry should be sent to/read from is not properly supported through
the store's interface, as it only applies to HTTP catalogs and not to local ones. To add a kinda hacky way to support
this, the following assumptions are made of the values received by the CRUD methods:

 - Read/Delete: since we only receive an Entry id when indicating what to read/delete, the remote catalog id this should
   be read from will come bundled with the entry id, with a prefix, like this "remote_catalog_id--entry_id".
   The "remote_catalog.py" module is used to extract this, and could be used to bundle it as well.
 - Create/Edit: besides the same bundling as above, in the entry_id field of the new entry's header, the catalog_id
   in the new entry's header will have the actual remote catalog id, and this is the value used.

"""

from __future__ import annotations

from typing import Any, List, Optional, OrderedDict

from mlte.catalog.model import CatalogEntry
from mlte.store.base import StoreURI
from mlte.store.catalog import remote_catalog
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.store_session import (
    CatalogEntryMapper,
    CatalogStoreSession,
)
from mlte.store.common.http_clients import OAuthHttpClient
from mlte.store.common.http_storage import HttpResourceStorage
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

        self.storage = HttpResourceStorage(
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
        self, *, storage: HttpResourceStorage, read_only: bool = False
    ) -> None:
        self.storage = storage
        """HTTP storage"""

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

    def __init__(self, storage: HttpResourceStorage) -> None:
        self.storage = storage
        """The HTTP storage access."""

    def create(
        self, new_entry: CatalogEntry, context: Any = None
    ) -> CatalogEntry:
        """This method assumes that the caller put in catalog_id the id of the remote catalog it would be stored into."""
        new_entry = remote_catalog.remove_remote_catalog_id(new_entry)
        response = self.storage.post(
            json=new_entry.to_json(),
            groups=_entry_group(new_entry.header.catalog_id),
        )
        return CatalogEntry(**response)

    def edit(
        self, edited_entry: CatalogEntry, context: Any = None
    ) -> CatalogEntry:
        """This method assumes that the caller put in catalog_id the id of the remote catalog it would be stored into."""
        edited_entry = remote_catalog.remove_remote_catalog_id(edited_entry)
        response = self.storage.put(
            json=edited_entry.to_json(),
            groups=_entry_group(edited_entry.header.catalog_id),
        )
        return CatalogEntry(**response)

    def read(
        self, catalog_and_entry_id: str, context: Any = None
    ) -> CatalogEntry:
        """This method assumes that the caller prefixed the entry_id with the local catalog id."""
        catalog_id, entry_id = remote_catalog.split_ids(catalog_and_entry_id)
        response = self.storage.get(
            id=entry_id, groups=_entry_group(catalog_id)
        )
        return CatalogEntry(**response)

    def list(self, context: Any = None) -> List[str]:
        entries = self.list_details()
        return [entry.header.identifier for entry in entries]

    def delete(
        self, catalog_and_entry_id: str, context: Any = None
    ) -> CatalogEntry:
        """This method assumes that the caller prefixed the entry_id with the local catalog id."""
        local_catalog_id, entry_id = remote_catalog.split_ids(
            catalog_and_entry_id
        )
        response = self.storage.delete(
            id=entry_id, groups=_entry_group(local_catalog_id)
        )
        return CatalogEntry(**response)

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
        return [CatalogEntry(**entry) for entry in response][
            offset : offset + limit
        ]


def _entry_group(catalog_id: Optional[str]) -> OrderedDict[str, str]:
    """Returns the resource group info for entries inside a catalog."""
    if not catalog_id:
        raise RuntimeError(
            "Can't create catalog group for entry with an empty catalog id."
        )
    return OrderedDict([(catalog_id, ENTRY_URL_KEY)])
