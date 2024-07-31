"""
test/backend/api/endpoints/artifact/test_artifact.py

Test the API for artifacts.
"""
from __future__ import annotations

import typing
from typing import Any

import pytest

from mlte.artifact.model import ArtifactModel
from mlte.artifact.type import ArtifactType
from mlte.backend.api import codes
from mlte.backend.api.model import WriteArtifactRequest
from mlte.model.base_model import BaseModel
from mlte.store.common.query import Query
from mlte.user.model import ResourceType, UserWithPassword
from test.backend.api.endpoints.artifact.test_model import (
    create_sample_model_using_admin,
    get_sample_model,
)
from test.backend.api.endpoints.artifact.test_version import (
    VERSION_URI,
    create_sample_version_using_admin,
    get_sample_version,
)
from test.backend.fixture import user_generator
from test.backend.fixture.test_api import TestAPI
from test.fixture.artifact import ArtifactFactory

ARTIFACT_ENDPOINT = "/artifact"
ARTIFACT_URI = f"{VERSION_URI}" + "/{}" + f"{ARTIFACT_ENDPOINT}"
DEFAULT_ARTIFACT_ID = "id0"


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------


def create_context(test_api: TestAPI) -> None:
    """Create context for artifacts.."""
    create_sample_model_using_admin(test_api)
    create_sample_version_using_admin(test_api)


def create_artifact_using_admin(
    artifact: ArtifactModel, test_api: TestAPI
) -> dict[str, Any]:
    """Create aftifact."""
    request = WriteArtifactRequest(artifact=artifact)
    return test_api.admin_create_entity(
        typing.cast(BaseModel, request),
        ARTIFACT_URI.format(
            get_sample_model().identifier, get_sample_version().identifier
        ),
    )


# -----------------------------------------------------------------------------
# Tests
# TODO: We should add versions to test that lack of permissions are working properly
# but that would increase the number of tests too much.
# -----------------------------------------------------------------------------


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_write(
    test_api_fixture,
    api_user: UserWithPassword,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be written."""
    model = get_sample_model()
    version = get_sample_version()
    test_api: TestAPI = test_api_fixture(api_user)
    create_context(test_api)
    test_client = test_api.get_test_client()

    a = ArtifactFactory.make(artifact_type)
    r = WriteArtifactRequest(artifact=a)
    res = test_client.post(
        ARTIFACT_URI.format(model.identifier, version.identifier),
        json=r.model_dump(),
    )
    assert res.status_code == codes.OK


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_read(
    test_api_fixture,
    api_user: UserWithPassword,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be read."""
    model = get_sample_model()
    version = get_sample_version()
    test_api: TestAPI = test_api_fixture(api_user)
    create_context(test_api)
    test_client = test_api.get_test_client()

    art_model = ArtifactFactory.make(artifact_type, id=DEFAULT_ARTIFACT_ID)
    art_json = create_artifact_using_admin(art_model, test_api)
    artifact = art_json["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.get(
        f"{ARTIFACT_URI.format(model.identifier, version.identifier)}/{created.header.identifier}"
    )
    assert res.status_code == codes.OK
    read = ArtifactModel(**res.json())
    assert read == created


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_read_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_list(
    test_api_fixture,
    api_user: UserWithPassword,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be searched."""
    model = get_sample_model()
    version = get_sample_version()
    test_api: TestAPI = test_api_fixture(api_user)
    create_context(test_api)
    test_client = test_api.get_test_client()

    art_model = ArtifactFactory.make(artifact_type, id=DEFAULT_ARTIFACT_ID)
    art_json = create_artifact_using_admin(art_model, test_api)
    artifact = art_json["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.get(
        f"{ARTIFACT_URI.format(model.identifier, version.identifier)}"
    )
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 1

    read = ArtifactModel(**collection[0])
    assert read == created


# TODO: note that this is tested with write permissions, since search uses post, and that is interperted as write.
@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_search(
    test_api_fixture,
    api_user: UserWithPassword,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be searched."""
    model = get_sample_model()
    version = get_sample_version()
    test_api: TestAPI = test_api_fixture(api_user)
    create_context(test_api)
    test_client = test_api.get_test_client()

    art_model = ArtifactFactory.make(artifact_type, id=DEFAULT_ARTIFACT_ID)
    art_json = create_artifact_using_admin(art_model, test_api)
    artifact = art_json["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.post(
        f"{ARTIFACT_URI.format(model.identifier, version.identifier)}/search",
        json=Query().model_dump(),
    )
    assert res.status_code == codes.OK

    collection = res.json()
    assert len(collection) == 1

    read = ArtifactModel(**collection[0])
    assert read == created


@pytest.mark.parametrize(
    "api_user",
    user_generator.get_test_users_with_write_permissions(
        ResourceType.MODEL, resource_id=get_sample_model().identifier
    ),
)
@pytest.mark.parametrize("artifact_type", ArtifactType)
def test_delete(
    test_api_fixture,
    api_user: UserWithPassword,
    artifact_type: ArtifactType,
) -> None:
    """Artifacts can be deleted."""
    model = get_sample_model()
    version = get_sample_version()
    test_api: TestAPI = test_api_fixture(api_user)
    create_context(test_api)
    test_client = test_api.get_test_client()

    art_model = ArtifactFactory.make(artifact_type, id=DEFAULT_ARTIFACT_ID)
    art_json = create_artifact_using_admin(art_model, test_api)
    artifact = art_json["artifact"]
    created = ArtifactModel(**artifact)

    res = test_client.delete(
        f"{ARTIFACT_URI.format(model.identifier, version.identifier)}/{created.header.identifier}"
    )
    assert res.status_code == codes.OK

    admin_client = test_api.get_test_client_for_admin()
    res = admin_client.get(
        f"{ARTIFACT_URI.format(model.identifier, version.identifier)}/{created.header.identifier}"
    )
    assert res.status_code == codes.NOT_FOUND
