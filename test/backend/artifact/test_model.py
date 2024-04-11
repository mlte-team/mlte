"""
test/backend/contex/test_model.py

Test the HTTP interface for model operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.context.model import Model, ModelCreate

from ..fixture.http import (  # noqa
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

    model = ModelCreate(identifier="model")

    res = client.post(f"{settings.API_PREFIX}/model", json=model.model_dump())
    assert res.status_code == codes.OK
    _ = Model(**res.json())


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

    res = client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1

    res = client.delete(f"{settings.API_PREFIX}/model/{model_id}")
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model")
    assert res.status_code == codes.OK
    assert len(res.json()) == 0
