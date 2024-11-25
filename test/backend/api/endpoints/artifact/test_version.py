"""
test/backend/api/endpoints/artifact/test_version.py

Test the API for version operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.context.model import Version, VersionCreate
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.api.endpoints.artifact.test_model import (
    MODEL_URI,
    create_fake_model_using_admin,
    create_sample_model_using_admin,
    get_sample_model,
)
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI

VERSION_ENDPOINT = "/version"
VERSION_URI = f"{MODEL_URI}" + "/{}" + f"{VERSION_ENDPOINT}"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_sample_version() -> VersionCreate:
    """Creates a simple test version."""
    version_id = "1.1"
    return VersionCreate(identifier=version_id)


def create_sample_version_using_admin(test_api: TestAPI) -> None:
    """Create sample model."""
    test_api.admin_create_entity(
        get_sample_version(), VERSION_URI.format(get_sample_model().identifier)
    )


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Versions can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version_id = "0"
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    version = VersionCreate(identifier=version_id)
    res = test_client.post(
        VERSION_URI.format(model.identifier),
        json=version.to_json(),
    )
    assert res.status_code == codes.OK
    _ = Version(**res.json())


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_create_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permission to create version."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version_id = "0"
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    version = VersionCreate(identifier=version_id)
    res = test_client.post(
        VERSION_URI.format(model.identifier),
        json=version.to_json(),
    )
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:
    """Versions can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version = get_sample_version()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(
        f"{VERSION_URI.format(model.identifier)}/{version.identifier}"
    )
    assert res.status_code == codes.OK
    read = Version(**res.json())
    assert read == Version(**version.to_json())


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to read versions."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version = get_sample_version()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(
        f"{VERSION_URI.format(model.identifier)}/{version.identifier}"
    )
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_list(test_api_fixture, api_user: UserWithPassword) -> None:
    """Versions can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(VERSION_URI.format(model.identifier))
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to list versions."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(VERSION_URI.format(model.identifier))
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:
    """Versions can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version = get_sample_version()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.delete(
        f"{VERSION_URI.format(model.identifier)}/{version.identifier}"
    )
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(
        f"{VERSION_URI.format(model.identifier)}/{version.identifier}"
    )
    assert res.status_code == codes.NOT_FOUND


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_delete_no_permissions(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to delete versions."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    version = get_sample_version()

    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.delete(
        f"{VERSION_URI.format(model.identifier)}/{version.identifier}"
    )
    assert res.status_code == codes.FORBIDDEN
