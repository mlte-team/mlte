"""
test/backend/api/endpoints/artifact/test_artifact.py

Test the API for artifacts.
"""

import pytest

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.backend.api import codes
from mlte.backend.api.model import WriteArtifactRequest
from mlte.backend.core.config import settings
from mlte.context.model import ModelCreate, VersionCreate
from mlte.store.artifact.query import Query
from test.backend.fixture.http import FastAPITestHttpClient
from test.fixture.artifact import ArtifactFactory

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def create_context(
    model_id: str, version_id: str, test_client: FastAPITestHttpClient
) -> None:
    """Create context for artifacts.."""
    res = test_client.post(
        f"{settings.API_PREFIX}/model",
        json=ModelCreate(identifier=model_id).model_dump(),
    )
    assert res.status_code == codes.OK

    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version",
        json=VersionCreate(identifier=version_id).model_dump(),
    )
    assert res.status_code == codes.OK


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------


def test_init(
    test_client: FastAPITestHttpClient,
) -> None:
    """The server can initialize."""
    res = test_client.get(f"{settings.API_PREFIX}/healthz")
    assert res.status_code == codes.OK


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_write(
    test_client: FastAPITestHttpClient,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be written."""

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, test_client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_read(
    test_client: FastAPITestHttpClient,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be read."""

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, test_client)

    a = ArtifactFactory.make(artifact_type, id="id0")
    r = WriteArtifactRequest(artifact=a)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK
    read = ArtifactModel(**res.json())
    assert read == created


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_search(
    test_client: FastAPITestHttpClient,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be searched."""
    model_id, version_id = "0", "0"
    create_context(model_id, version_id, test_client)

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK
    artifact = res.json()["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/search",
        json=Query().model_dump(),
    )
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 1

    read = ArtifactModel(**collection[0])
    assert read == created


@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_delete(
    test_client: FastAPITestHttpClient,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be deleted."""

    model_id, version_id = "0", "0"
    create_context(model_id, version_id, test_client)

    a = ArtifactFactory.make(artifact_type, "id0")
    r = WriteArtifactRequest(artifact=a)
    res = test_client.post(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact",
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK

    res = test_client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK

    res = test_client.delete(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == codes.OK

    res = test_client.get(
        f"{settings.API_PREFIX}/model/{model_id}/version/{version_id}/artifact/id0"
    )
    assert res.status_code == 404
