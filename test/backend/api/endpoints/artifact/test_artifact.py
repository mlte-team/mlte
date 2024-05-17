"""
test/backend/artifcat/test_negotiation_card.py

Test the HTTP interface for negotiation card operations.
"""

import pytest

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.backend.api import codes
from mlte.backend.api.model import WriteArtifactRequest
from mlte.backend.core.config import settings
from mlte.context.model import ModelCreate, VersionCreate
from mlte.store.artifact.query import Query
from test.backend.fixture.http import (  # noqa
    FastAPITestHttpClient,
    clients_and_types,
    mem_store_and_test_http_client,
)
from test.fixture.artifact import ArtifactFactory


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_init(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """The server can initialize."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)
    res = client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_write(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be written."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_read(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be read."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type, id="id0")
    r = WriteArtifactRequest(artifact=a)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK
    read = ArtifactModel(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_search(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be searched."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/search",
        json=Query().model_dump(),
    )
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 1

    read = ArtifactModel(**collection[0])
    assert read == created


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_delete(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be deleted."""
    client: FastAPITestHttpClient = request.getfixturevalue(client_fixture)

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type, "id0")
    r = WriteArtifactRequest(artifact=a)
    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK

    res = client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK

    res = client.delete(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK

    res = client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 404


def create_context(
    model_id: str, version_id: str, client: FastAPITestHttpClient
) -> None:
    """Create context for artifacts.."""
    res = client.post(
        f"{settings.API_PREFIX}/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == codes.OK

    res = client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=VersionCreate(identifier=version_id).model_dump(),
    )
    assert res.status_code == codes.OK
