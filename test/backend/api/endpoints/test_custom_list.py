"""
test/backend/api/endpoints/test_custom_list.py

Test the API for custom list operations.
"""

from typing import Any

import pytest

from mlte.backend.api import codes
from mlte.custom_list.custom_list_names import CustomListName
from mlte.custom_list.model import CustomListEntryModel
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.custom_list.fixture import get_custom_list_uri, get_test_entry

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def create_entry_using_admin(
    custom_list_id: CustomListName, entry: CustomListEntryModel, api: TestAPI
):
    """Create test entry using admin."""
    url = get_custom_list_uri(custom_list_id=custom_list_id)
    api.admin_create_entity(entry, url)


def get_entry_using_admin(
    custom_list_id: str, entry_id: str, api: TestAPI
) -> dict[str, Any]:
    """Gets a custom list entry using admin."""
    if custom_list_id is None:
        raise Exception("Error running test, custom list id can't be null")

    # this isnt fixed yet
    # url = get_entry_uri(custom_list_id=custom_list_id, entry_id=entry_id)
    url = get_custom_list_uri(custom_list_id=custom_list_id)
    return api.admin_read_entity(entry_id, url)


# -----------------------------------------------------------------------------
# Tests - Create
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test custom list entries can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Test creating an entry in list without parent entries
    parent_url = get_custom_list_uri(CustomListName.QA_CATEGORIES)
    parent_entry = get_test_entry()

    res = test_client.post(parent_url, json=parent_entry.to_json())
    assert res.status_code == codes.OK
    _ = CustomListEntryModel(**res.json())

    # Test creating an entry in list with parent entries
    child_url = get_custom_list_uri(CustomListName.QUALITY_ATTRIBUTES)
    child_entry = get_test_entry(
        name="child", description="child desc", parent=parent_entry.name
    )

    res = test_client.post(child_url, json=child_entry.to_json())
    assert res.status_code == codes.OK
    _ = CustomListEntryModel(**res.json())


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_create_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to create."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES)
    res = test_client.post(f"{url}", json=entry.to_json())
    assert res.status_code == codes.FORBIDDEN


# -----------------------------------------------------------------------------
# Tests - Read
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test custom list entries can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Create entry to read
    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    # Read entry
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES, entry.name)
    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    _ = CustomListEntryModel(**res.json())


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to read entry."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Create entry to read
    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    # Read entry
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES, entry.name)
    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


# -----------------------------------------------------------------------------
# Tests - Edit
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_edit(test_api_fixture, api_user: UserWithPassword) -> None:
    """Entries can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Create test entry.
    entry = get_test_entry()
    desc2 = "new description"
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    # Edit entry.
    entry.description = desc2
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES)
    res = test_client.put(f"{url}", json=entry.to_json())
    assert res.status_code == codes.OK

    # Read it back.
    edited_entry = CustomListEntryModel(
        **get_entry_using_admin(
            CustomListName.QA_CATEGORIES, entry.name, test_api
        )
    )
    assert edited_entry.description == entry.description


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_edit_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to edit."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    # Create test entry.
    entry = get_test_entry()
    desc2 = "new description"
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    # Edit entry.
    entry.description = desc2
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES)
    res = test_client.put(f"{url}", json=entry.to_json())
    assert res.status_code == codes.FORBIDDEN


# -----------------------------------------------------------------------------
# Tests - List
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_list_lists(test_api_fixture, api_user: UserWithPassword) -> None:
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
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_list_lists_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to list lists."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    url = get_custom_list_uri()
    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_list_single_list(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test that a list can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    url = get_custom_list_uri(
        custom_list_id=CustomListName.QA_CATEGORIES, no_entry=True
    )
    original_entries = test_client.get(f"{url}")
    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_entries.json()) + 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_list_single_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to list single list."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    url = get_custom_list_uri(
        custom_list_id=CustomListName.QA_CATEGORIES, no_entry=True
    )
    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


# -----------------------------------------------------------------------------
# Tests - Delete
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:
    """Test entries can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    url = get_custom_list_uri(CustomListName.QA_CATEGORIES, entry.name)
    res = test_client.delete(f"{url}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{url}")
    assert res.status_code == codes.NOT_FOUND

    # Make child and parent entries
    parent_entry = get_test_entry()
    create_entry_using_admin(
        CustomListName.QA_CATEGORIES, parent_entry, test_api
    )
    child_entry = get_test_entry(
        name="child", description="child desc", parent=parent_entry.name
    )
    create_entry_using_admin(
        CustomListName.QUALITY_ATTRIBUTES, child_entry, test_api
    )

    # Test parent is deleted
    url = get_custom_list_uri(CustomListName.QA_CATEGORIES, parent_entry.name)
    res = test_client.delete(f"{url}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{url}")
    assert res.status_code == codes.NOT_FOUND

    # Test deletion cascades to children
    url = get_custom_list_uri(
        CustomListName.QUALITY_ATTRIBUTES, child_entry.name
    )
    res = admin_client.get(f"{url}")
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CUSTOM_LIST
    ),
)
def test_delete_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to delete."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(CustomListName.QA_CATEGORIES, entry, test_api)

    url = get_custom_list_uri(CustomListName.QA_CATEGORIES, entry.name)
    res = test_client.delete(f"{url}")
    assert res.status_code == codes.FORBIDDEN
