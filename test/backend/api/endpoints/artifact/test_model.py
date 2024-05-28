"""
test/backend/api/endpoints/artifact/test_model.py

Test the API for model operations.
"""

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.context.model import Model, ModelCreate
from mlte.store.user.store_session import ManagedUserSession
from test.backend.fixture.http import FastAPITestHttpClient


def test_init(test_client: FastAPITestHttpClient) -> None:
    """The server can initialize."""
    res = test_client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


def test_create(test_client: FastAPITestHttpClient) -> None:
    """Models can be created."""
    original_perms = []
    original_groups = []
    with ManagedUserSession(state.user_store.session()) as user_store:
        original_perms = user_store.permission_mapper.list()
        original_groups = user_store.group_mapper.list()

    model = ModelCreate(identifier="model")

    res = test_client.post(
        f"{settings.API_PREFIX}/model", json=model.model_dump()
    )
    assert res.status_code == codes.OK
    _ = Model(**res.json())

    # Also test that permissions and groups were created.
    new_perms = []
    new_groups = []
    with ManagedUserSession(state.user_store.session()) as user_store:
        new_perms = user_store.permission_mapper.list()
        new_groups = user_store.group_mapper.list()

    assert len(original_perms) + 5 == len(new_perms)
    assert len(original_groups) + 2 == len(new_groups)


def test_read(test_client: FastAPITestHttpClient) -> None:
    """Models can be read."""
    model_id = "0"
    model = ModelCreate(identifier=model_id)
    res = test_client.post(
        f"{settings.API_PREFIX}/model", json=model.model_dump()
    )
    assert res.status_code == codes.OK

    created = Model(**res.json())

    res = test_client.get(f"{settings.API_PREFIX}/model/{model_id}")
    assert res.status_code == codes.OK
    read = Model(**res.json())
    assert read == created


def test_list(
    test_client: FastAPITestHttpClient,
) -> None:
    """Models can be listed."""
    model_id = "0"
    model = ModelCreate(identifier=model_id)

    res = test_client.post(
        f"{settings.API_PREFIX}/model", json=model.model_dump()
    )
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


def test_delete(
    test_client: FastAPITestHttpClient,
) -> None:
    """Models can be deleted."""
    model_id = "0"
    model = ModelCreate(identifier=model_id)

    res = test_client.post(
        f"{settings.API_PREFIX}/model", json=model.model_dump()
    )
    assert res.status_code == codes.OK

    num_original_perms = 0
    num_original_groups = 0
    with ManagedUserSession(state.user_store.session()) as user_store:
        num_original_perms = len(user_store.permission_mapper.list())
        num_original_groups = len(user_store.group_mapper.list())

    res = test_client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1

    res = test_client.delete(f"{settings.API_PREFIX}/model/{model_id}")
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 0

    # Also test that permissions and groups were delete.
    num_new_perms = 0
    num_new_groups = 0
    with ManagedUserSession(state.user_store.session()) as user_store:
        num_new_perms = len(user_store.permission_mapper.list())
        num_new_groups = len(user_store.group_mapper.list())

    assert num_original_perms - 5 == num_new_perms
    assert num_original_groups - 2 == num_new_groups
