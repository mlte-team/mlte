"""
test/store/catalog/fixture.py

Fixtures for MLTE catalog store unit tests.
"""

from __future__ import annotations

import typing
from enum import auto
from typing import Generator, Optional

import pytest
from strenum import StrEnum

from mlte.backend.core.config import settings
from mlte.catalog.model import (
    CatalogEntry,
    CatalogEntryHeader,
    CatalogEntryType,
)
from mlte.store.catalog.store import CatalogStore
from mlte.store.catalog.underlying.http import (
    HTTPCatalogGroupEntryMapper,
    HttpCatalogGroupStore,
)
from mlte.user.model import ResourceType
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.catalog.catalog_store_creators import (
    create_fs_store,
    create_http_store,
    create_memory_store,
    create_rdbs_store,
)

CATALOG_BASE_URI = f"{settings.API_PREFIX}/{ResourceType.CATALOG_ENTRY.value}"
"""Base URI for catalogs."""

DEFAULT_ENTRY_ID = "e1"
DEFAULT_ENTRY_DESC = "Code sample"
DEFAULT_ENTRY_CODE = "print('hello')"
DEFAULT_ENTRY_TYPE = CatalogEntryType.MEASUREMENT
TEST_CATALOG_ID = "cat1"
"""Default values."""


class CatalogStoreType(StrEnum):
    """Store types."""

    MEMORY_STORE = auto()
    FS_STORE = auto()
    RDBS_STORE = auto()
    HTTP_STORE = auto()


def catalog_stores() -> Generator[str, None, None]:
    """
    Yield catalog store fixture names.
    :return: Store fixture name
    """
    for store_fixture_name in CatalogStoreType:
        yield store_fixture_name.value


def create_api_and_http_store() -> HttpCatalogGroupStore:
    """
    Get a RemoteHttpStore configured with a test client.
    :return: The configured store
    """
    # Set an in memory store and get a test http client, configured for the app.
    user = user_generator.build_admin_user()
    test_api = TestAPI(user=user, default_catalog_id=TEST_CATALOG_ID)
    client = test_api.get_test_client()

    return create_http_store(
        username=client.username,
        password=client.password,
        uri=str(client.client.base_url),
        client=client,
    )


@pytest.fixture(scope="function")
def create_test_store(tmpdir_factory) -> typing.Callable[[str], CatalogStore]:
    def _make(store_fixture_name) -> CatalogStore:
        if store_fixture_name == CatalogStoreType.MEMORY_STORE:
            return create_memory_store()
        elif store_fixture_name == CatalogStoreType.FS_STORE:
            return create_fs_store(tmpdir_factory.mktemp("data"))
        elif store_fixture_name == CatalogStoreType.RDBS_STORE:
            return create_rdbs_store()
        elif store_fixture_name == CatalogStoreType.HTTP_STORE:
            return create_api_and_http_store()
        else:
            raise RuntimeError(
                f"Invalid store type received: {store_fixture_name}"
            )

    return _make


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_entry_uri(
    catalog_id: Optional[str] = None, entry_id: Optional[str] = None
):
    """Returns a proper URI for the endpoint based on the presence of the ids."""
    url = f"{CATALOG_BASE_URI}"
    if catalog_id is None:
        url = f"{url}s/entry"
    else:
        url = f"{url}/{catalog_id}/entry"
        if entry_id is not None:
            url = f"{url}/{entry_id}"
    return url


def get_test_entry(
    id: str = DEFAULT_ENTRY_ID,
    description: str = DEFAULT_ENTRY_DESC,
    code: str = DEFAULT_ENTRY_CODE,
    code_type: CatalogEntryType = DEFAULT_ENTRY_TYPE,
    catalog_id: str = TEST_CATALOG_ID,
) -> CatalogEntry:
    """Helper to get an entry structure."""
    id = id
    description = description
    code = code
    header = CatalogEntryHeader(identifier=id, catalog_id=catalog_id)
    test_entry = CatalogEntry(
        header=header,
        code=code,
        description=description,
        code_type=code_type,
    )

    return test_entry


def get_test_entry_for_store(
    id: str = DEFAULT_ENTRY_ID,
    description: str = DEFAULT_ENTRY_DESC,
    code: str = DEFAULT_ENTRY_CODE,
    code_type: CatalogEntryType = DEFAULT_ENTRY_TYPE,
    catalog_id: str = TEST_CATALOG_ID,
    store_name: str = "",
) -> CatalogEntry:
    """Helper to get an entry structure."""
    entry = get_test_entry(id, description, code, code_type, catalog_id)

    if store_name == CatalogStoreType.HTTP_STORE.value:
        entry.header.identifier = (
            HTTPCatalogGroupEntryMapper.generate_composite_id(
                entry.header.catalog_id, entry.header.identifier
            )
        )

    return entry
