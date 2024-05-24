"""
test/backend/contex/test_model.py

Test the HTTP interface for model operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.backend.state import state
from mlte.context.model import Model, ModelCreate
from mlte.store.user.store_session import ManagedUserSession
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)

# -----------------------------------------------------------------------------
# Tests: Model
# -----------------------------------------------------------------------------


@pytest.mark.parametrize("client_fixture", clients())
def test_init(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """The server can initialize."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    res = client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


@pytest.mark.parametrize("client_fixture", clients())
def test_create(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    original_perms = []
    original_groups = []
    with ManagedUserSession(state.user_store.session()) as user_store:
        original_perms = user_store.permission_mapper.list()
        original_groups = user_store.group_mapper.list()

    model = ModelCreate(identifier="model")

    res = client.post(f"{settings.API_PREFIX}/model", json=model.model_dump())
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


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id = "0"
    model = ModelCreate(identifier=model_id)
    res = client.post(f"{settings.API_PREFIX}/model", json=model.model_dump())
    assert res.status_code == codes.OK

    created = Model(**res.json())

    res = client.get(f"{settings.API_PREFIX}/model/{model_id}")
    assert res.status_code == codes.OK
    read = Model(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id = "0"
    model = ModelCreate(identifier=model_id)

    res = client.post(f"{settings.API_PREFIX}/model", json=model.model_dump())
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Models can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id = "0"
    model = ModelCreate(identifier=model_id)

    res = client.post(f"{settings.API_PREFIX}/model", json=model.model_dump())
    assert res.status_code == codes.OK

    num_original_perms = 0
    num_original_groups = 0
    with ManagedUserSession(state.user_store.session()) as user_store:
        num_original_perms = len(user_store.permission_mapper.list())
        num_original_groups = len(user_store.group_mapper.list())

    res = client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1

    res = client.delete(f"{settings.API_PREFIX}/model/{model_id}")
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model")
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
