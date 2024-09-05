"""
test/backend/api/endpoints/test_catalog_entry.py

Test the API for catalog operations.
"""
from __future__ import annotations

import pytest

from mlte.backend.api import codes
from mlte.catalog.model import CatalogEntry
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.catalog.fixture import get_entry_uri, get_test_entry

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.CATALOG_ENTRY
    ),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Catalog entries can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()

    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    print(url)
    res = test_client.post(f"{url}", json=entry.model_dump())
    print(res)
    assert res.status_code == codes.OK
    _ = CatalogEntry(**res.json())
