"""
test/web/store/artifcat/test_negotiation_card.py

Test the HTTP interface for negotiation card operations.
"""

import pytest
from fastapi.testclient import TestClient

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.store.query import Query
from mlte.web.store.api.model import WriteArtifactRequest

from ...fixture.artifact import ArtifactFactory
from .fixure.http import clients_and_types, mem_client  # noqa


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_init(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """The server can initialize."""
    client: TestClient = request.getfixturevalue(client_fixture)
    res = client.get("/api/healthz")
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_write(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be written."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a, parents=False)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == 200


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_read(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be read."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type, id="id0")
    r = WriteArtifactRequest(artifact=a, parents=False)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == 200
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 200
    read = ArtifactModel(**res.json())
    assert read == created


@pytest.mark.parametrize("client_fixture,artifact_type", clients_and_types())
def test_search(
    client_fixture: str,
    artifact_type: ArtifactType,
    request: pytest.FixtureRequest,
) -> None:  # noqa
    """Artifacts can be searched."""
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a, parents=False)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == 200
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/search",
        json=Query().model_dump(),
    )
    assert res.status_code == 200

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
    client: TestClient = request.getfixturevalue(client_fixture)

    namespace_id, model_id, version_id = "0", "0", "0"
    create_context(namespace_id, model_id, version_id, client)

    a = ArtifactFactory.make(artifact_type, "id0")
    r = WriteArtifactRequest(artifact=a, parents=False)
    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 200

    res = client.delete(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 200

    res = client.get(
        f"/api/namespace/{namespace_id}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 404


def create_context(
    namespace_id: str, model_id: str, version_id: str, client: TestClient
) -> None:
    """Create context for artifacts.."""
    res = client.post(
        "/api/namespace",
        json=NamespaceCreate(identifier=namespace_id).model_dump(),
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == 200

    res = client.post(
        f"/api/namespace/{namespace_id}/model/{model_id}/version",
        json=VersionCreate(identifier=version_id).model_dump(),
    )
    assert res.status_code == 200
