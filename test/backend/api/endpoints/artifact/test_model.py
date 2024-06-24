"""
test/backend/api/endpoints/artifact/test_model.py

Test the API for model operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.context.model import Model, ModelCreate
from mlte.store.user.policy import Policy
from mlte.store.user.store_session import ManagedUserSession
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI

MODEL_ENDPOINT = "/model"
MODEL_URI = f"{settings.API_PREFIX}{MODEL_ENDPOINT}"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def get_sample_model() -> ModelCreate:
    """Creates a simple test model."""
    model_id = "m0"
    return ModelCreate(identifier=model_id)


def create_sample_model_using_admin(test_api: TestAPI) -> None:
    """Create sample model."""
    test_api.admin_create_entity(get_sample_model(), MODEL_URI)


def create_fake_model_using_admin(test_api: TestAPI) -> None:
    """Create fake model used in wrong permission tests."""
    test_api.admin_create_entity(
        ModelCreate(identifier=user_generator.FAKE_ID), MODEL_URI
    )


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_health(
    test_api_fixture,
    api_user: UserWithPassword = user_generator.build_test_user(),
) -> None:
    """The server can initialize."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()
    res = test_client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(ResourceType.MODEL),
)
def test_create(test_api_fixture, api_user: UserWithPassword) -> None:
    """Models can be created."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    model = ModelCreate(identifier="model")

    res = test_client.post(MODEL_URI, json=model.model_dump())
    assert res.status_code == codes.OK
    _ = Model(**res.json())

    # Also test that permissions and groups were created.
    with ManagedUserSession(state.user_store.session()) as user_store:
        assert Policy.is_stored(
            ResourceType.MODEL, model.identifier, user_store
        )


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(ResourceType.MODEL),
)
def test_create_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to create model."""
    test_api: TestAPI = test_api_fixture(api_user)
    test_client = test_api.get_test_client()

    model = ModelCreate(identifier="model")

    res = test_client.post(MODEL_URI, json=model.model_dump())
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_read(test_api_fixture, api_user: UserWithPassword) -> None:
    """Models can be read."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(f"{MODEL_URI}/{model.identifier}")
    assert res.status_code == codes.OK
    read = Model(**res.json())
    assert read == Model(**model.model_dump(), versions=[])


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_read_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to read models."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(f"{MODEL_URI}/{model.identifier}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(ResourceType.MODEL),
)
def test_list(test_api_fixture, api_user: UserWithPassword) -> None:
    """Models can be listed."""
    test_api: TestAPI = test_api_fixture(api_user)
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(f"{MODEL_URI}")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_read_permissions(ResourceType.MODEL),
)
def test_list_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to list models."""
    test_api: TestAPI = test_api_fixture(api_user)
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.get(f"{MODEL_URI}")
    assert res.status_code == codes.FORBIDDEN


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_delete(test_api_fixture, api_user: UserWithPassword) -> None:
    """Models can be deleted."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.delete(f"{MODEL_URI}/{model.identifier}")
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(f"{MODEL_URI}/{model.identifier}")
    assert res.status_code == codes.NOT_FOUND

    # Also test that permissions and groups were deleted
    with ManagedUserSession(state.user_store.session()) as user_store:
        assert not Policy.is_stored(
            ResourceType.MODEL, model.identifier, user_store
        )


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_no_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
def test_delete_no_permission(
    test_api_fixture, api_user: UserWithPassword
) -> None:
    """No permissions to delete model."""
    test_api: TestAPI = test_api_fixture(api_user)
    model = get_sample_model()
    create_sample_model_using_admin(test_api)
    create_fake_model_using_admin(test_api)
    test_client = test_api.get_test_client()

    res = test_client.delete(f"{MODEL_URI}/{model.identifier}")
    assert res.status_code == codes.FORBIDDEN
