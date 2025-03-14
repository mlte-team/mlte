"""
test/backend/api/endpoints/test_custom_list.py

Test the API for custom list operations.
"""

import pytest

from typing import Any

from mlte.user.model import UserWithPassword, ResourceType
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.custom_list.fixture import get_test_entry, get_entry_uri
from mlte.custom_list.model import CustomListEntryModel, CustomListName
from mlte.backend.api import codes

CUSTOM_LIST_ENDPOINT = "/custom_list"
CUSTOM_LIST_URI = f"{settings.API_PREFIX}{CUSTOM_LIST_ENDPOINT}"



# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def create_entry_using_admin(custom_list_id: CustomListName, entry: CustomListEntryModel, api: TestAPI):
    """Create test entry using admin."""
    url = get_custom_list_uri(custom_list_id=custom_list_id)
    api.admin_create_entity(entry, url)

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.CUSTOM_LIST),
)
def test_list_lists(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Test that lists can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    url = get_custom_list_uri()
    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 2

@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.CUSTOM_LIST),
)
def test_list_single_list(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """Test that a list can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    url = get_custom_list_uri(custom_list_id=CustomListName.QA_CATEGORIES, no_entry=True)    
    original_entries = test_client.get(f"{url}")
    entry = get_test_entry(parent="")
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_entries.json()) + 1

    _ = CustomListEntryModel(**get_entry_using_admin(entry.name, test_api))