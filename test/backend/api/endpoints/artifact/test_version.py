"""
test/backend/context/test_version.py

Test the HTTP interface for version operations.
"""

import pytest

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.context.model import ModelCreate, Version, VersionCreate
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients,
    mem_store_and_test_http_client,
)


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
    """Versions can be created."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    model_id = "0"
    version_id = "0"
    create_model(model_id, client)

    version = VersionCreate(identifier=version_id)

    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK
    _ = Version(**res.json())


@pytest.mark.parametrize("client_fixture", clients())
def test_read(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    model_id = "0"
    version_id = "0"
    create_model(model_id, client)

    version = VersionCreate(identifier=version_id)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    created = Version(**res.json())

    res = client.get(f"{settings.API_PREFIX}/model/0/version/0")
    assert res.status_code == codes.OK
    read = Version(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture", clients())
def test_list(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be listed."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    model_id = "0"
    version_id = "0"
    create_model(model_id, client)

    version = VersionCreate(identifier=version_id)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


@pytest.mark.parametrize("client_fixture", clients())
def test_delete(
    client_fixture: str, request: pytest.FixtureRequest
) -> None:  # noqa
    """Versions can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    model_id = "0"
    version_id = "0"
    create_model(model_id, client)

    version = VersionCreate(identifier=version_id)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1

    res = client.delete(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
    )
    assert res.status_code == codes.OK

    res = client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 0


def create_model(model_id: str, client: FastAPITestHttpClient) -> None:
    """Create a model with the given identifier."""
    res = client.post(
        f"{settings.API_PREFIX}/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == codes.OK
