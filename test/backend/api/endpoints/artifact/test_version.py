"""
test/backend/context/test_version.py

Test the HTTP interface for version operations.
"""

from mlte.backend.api import codes
from mlte.backend.core.config import settings
from mlte.context.model import ModelCreate, Version, VersionCreate
from test.backend.fixture.http import FastAPITestHttpClient


def test_init(test_client: FastAPITestHttpClient) -> None:
    """The server can initialize."""
    res = test_client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


def test_create(test_client: FastAPITestHttpClient) -> None:
    """Versions can be created."""
    model_id = "0"
    version_id = "0"
    create_model(model_id, test_client)

    version = VersionCreate(identifier=version_id)

    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK
    _ = Version(**res.json())


def test_read(test_client: FastAPITestHttpClient) -> None:
    """Versions can be read."""
    model_id = "0"
    version_id = "0"
    create_model(model_id, test_client)

    version = VersionCreate(identifier=version_id)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    created = Version(**res.json())

    res = test_client.get(f"{settings.API_PREFIX}/model/0/version/0")
    assert res.status_code == codes.OK
    read = Version(**res.json())
    assert read == created


def test_list(test_client: FastAPITestHttpClient) -> None:
    """Versions can be listed."""
    model_id = "0"
    version_id = "0"
    create_model(model_id, test_client)

    version = VersionCreate(identifier=version_id)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1


def test_delete(test_client: FastAPITestHttpClient) -> None:
    """Versions can be deleted."""
    model_id = "0"
    version_id = "0"
    create_model(model_id, test_client)

    version = VersionCreate(identifier=version_id)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=version.model_dump(),
    )
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 1

    res = test_client.delete(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}"
    )
    assert res.status_code == codes.OK

    res = test_client.get(f"{settings.API_PREFIX}/model/{model_id}/version")
    assert res.status_code == codes.OK
    assert len(res.json()) == 0


def create_model(model_id: str, client: FastAPITestHttpClient) -> None:
    """Create a model with the given identifier."""
    res = client.post(
        f"{settings.API_PREFIX}/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == codes.OK
