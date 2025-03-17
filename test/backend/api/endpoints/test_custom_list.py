"""
test/backend/api/endpoints/test_custom_list.py

Test the API for custom list operations.
"""

from typing import Any, Optional

import pytest

from mlte.backend.api import codes
from mlte.custom_list.model import CustomListEntryModel, CustomListName
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.custom_list.fixture import get_custom_list_uri, get_test_entry

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def create_entry_using_admin(custom_list_id: CustomListName, entry: CustomListEntryModel, api: TestAPI):
    """Create test entry using admin."""
    url = get_custom_list_uri(custom_list_id=custom_list_id)
    api.admin_create_entity(entry, url)

def get_entry_using_admin(custom_list_id: str, entry_id: str, api: TestAPI) -> dict[str, Any]:
    """Gets a custom list entry using admin."""
    if custom_list_id is None:
        raise Exception("Error running test, custom list id can't be null")

    # this isnt fixed yet
    # url = get_entry_uri(custom_list_id=custom_list_id, entry_id=entry_id)
    url = get_custom_list_uri(custom_list_id=custom_list_id)
    print('in admin')
    print(url)
    return api.admin_read_entity(entry_id, url)

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.CUSTOM_LIST),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test custom list entries can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES)
    print(url)
    entry = get_test_entry(parent="")

    print(entry)
    print(test_client)

    res = test_client.post(url, json=entry.to_json())
    print("@@")
    print(res.text)
    print()
    assert res.status_code == codes.OK
    _ = CustomListEntryModel(**res.json())
    _ = CustomListEntryModel(**get_entry_using_admin(CustomListName.QA_CATEGORIES, entry.name, test_api))

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
