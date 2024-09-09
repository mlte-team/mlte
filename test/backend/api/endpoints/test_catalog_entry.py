"""
test/backend/api/endpoints/test_catalog_entry.py

Test the API for catalog operations.
"""
from __future__ import annotations

from typing import Any, Optional

import pytest

from mlte.backend.api import codes
from mlte.catalog.model import CatalogEntry
from mlte.store.query import Query
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.store.catalog.fixture import get_entry_uri, get_test_entry

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def create_entry_using_admin(entry: CatalogEntry, api: TestAPI):
    """Create test entry using admin."""
    entry.header.creator = user_generator.TEST_ADMIN_USERNAME
    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    api.admin_create_entity(entry, url)


def get_entry_using_admin(
    catalog_id: Optional[str], entry_id: str, api: TestAPI
) -> dict[str, Any]:
    """Gets an entry using admin."""
    if catalog_id is None:
        raise Exception("Error running test, catalog id can't be null")
    url = get_entry_uri(catalog_id)
    return api.admin_read_entity(entry_id, url)


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.CATALOG),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Catalog entries can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry(creator=api_user.username)

    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    res = test_client.post(f"{url}", json=entry.model_dump())
    assert res.status_code == codes.OK
    _ = CatalogEntry(**res.json())


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CATALOG
    ),
)
def test_create_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permissions to create."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()

    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    res = test_client.post(f"{url}", json=entry.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.CATALOG),
)
def test_edit(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Entries can be edited."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry(updater=api_user.username)
    desc2 = "new description"

    # Create test entry.
    create_entry_using_admin(entry, test_api)

    # Edit entry.
    entry.description = desc2
    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    res = test_client.put(f"{url}", json=entry.model_dump())
    assert res.status_code == codes.OK

    # Read it back.
    edited_catalog_entry = CatalogEntry(
        **get_entry_using_admin(
            entry.header.catalog_id, entry.header.identifier, test_api
        )
    )
    assert edited_catalog_entry.description == entry.description


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CATALOG
    ),
)
def test_edit_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permissions to edit."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()
    desc2 = "new description"

    # Create test entry.
    create_entry_using_admin(entry, test_api)

    # Edit entry.
    entry.description = desc2
    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    res = test_client.put(f"{url}", json=entry.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.CATALOG),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Entries can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()

    create_entry_using_admin(entry, test_api)

    url = get_entry_uri(
        catalog_id=entry.header.catalog_id, entry_id=entry.header.identifier
    )
    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    read = CatalogEntry(**res.json())
    read.header.created = -1  # To ignore times when comparing
    assert read == entry


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CATALOG
    ),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permission to read entry"""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(entry, test_api)

    url = get_entry_uri(
        catalog_id=entry.header.catalog_id, entry_id=entry.header.identifier
    )
    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.CATALOG),
)
def test_list(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Entries can be listed in a catalog."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()

    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    original_entries = test_client.get(f"{url}")

    create_entry_using_admin(entry, test_api)

    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_entries.json()) + 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CATALOG
    ),
)
def test_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permission to list."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    entry = get_test_entry()

    url = get_entry_uri(catalog_id=entry.header.catalog_id)
    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.CATALOG),
)
def test_list_all(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Entries can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    url = get_entry_uri()
    original_entries = test_client.get(f"{url}")

    entry = get_test_entry()
    create_entry_using_admin(entry, test_api)

    res = test_client.get(f"{url}")
    assert res.status_code == codes.OK
    assert len(res.json()) == len(original_entries.json()) + 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.CATALOG
    ),
)
def test_list_all_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:  # noqa
    """No permission to list."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    url = get_entry_uri()
    res = test_client.get(f"{url}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.CATALOG),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:  # noqa
    """Entries can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(entry, test_api)

    url = get_entry_uri(
        catalog_id=entry.header.catalog_id, entry_id=entry.header.identifier
    )
    res = test_client.delete(f"{url}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{url}")
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.CATALOG
    ),
)
def test_delete_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to delete."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(entry, test_api)

    url = get_entry_uri(
        catalog_id=entry.header.catalog_id, entry_id=entry.header.identifier
    )
    res = test_client.delete(f"{url}")
    assert res.status_code == codes.FORBIDDEN


# TODO: note that this is tested with write permissions, since search uses post, and that is interpreted as write.
@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.CATALOG),
)
def test_search(
    test_api_fixture,
    api_user: UserWithPassword,
) -> None:
    """Catalogs can be searched."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    entry = get_test_entry()
    create_entry_using_admin(entry, test_api)

    url = get_entry_uri()
    res = test_client.post(f"{url}/search", json=Query().model_dump())
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 1

    read = CatalogEntry(**collection[0])
    read.header.created = -1  # To ignore times when comparing
    assert read == entry
