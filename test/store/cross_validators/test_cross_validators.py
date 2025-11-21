"""Unit tests for CrossValidator functionality."""

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.session.session_stores import SessionStores, setup_stores
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.catalog.store_session import ManagedCatalogSession
from test.backend.fixture import test_api, user_generator
from test.fixture.artifact import ArtifactModelFactory
from test.store.artifact.test_underlying import check_artifact_writing
from test.store.catalog.fixture import get_test_entry_for_store
from test.backend.fixture.test_api import TestAPI
from test.store.defaults import IN_MEMORY_SQLITE_DB

URIS = [
    "memory://",
    IN_MEMORY_SQLITE_DB
]
MODEL_ID = "model0"
VERISON_ID = "version0"
ARTIFACT_ID = "myid"
VALID_USER = "admin"
INVALID_USER = "not a user"


@pytest.mark.parametrize("store_uri", URIS)
def test_artifact_cross_validators(store_uri: str):
    """Test artifact cross validators."""

    print(store_uri)
    stores = setup_stores(store_uri)

    with ManagedArtifactSession(stores.artifact_store.session()) as artifact_store:
        artifact_store.model_mapper.create(Model(identifier=MODEL_ID))
        artifact_store.version_mapper.create(
            Version(identifier=VERISON_ID), MODEL_ID
        )
        
        artifact = ArtifactModelFactory.make(ArtifactType.NEGOTIATION_CARD, ARTIFACT_ID)
        artifact_id = artifact.header.identifier

        # Valid submission
        _ = check_artifact_writing(
            artifact_store, MODEL_ID, VERISON_ID, artifact_id, artifact, VALID_USER
        )

        # Invalid user submission
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store, MODEL_ID, VERISON_ID, artifact_id, artifact, INVALID_USER
            ) 

        # Invalid quality attribute submission
        artifact.body.system_requirements[0].quality = "not a quality attribute"
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store, MODEL_ID, VERISON_ID, artifact_id, artifact, VALID_USER
            )

        # TODO: make sure this is create and edit


@pytest.mark.parametrize("store_uri", URIS)
def test_catalog_cross_validators(store_uri: str):
    """Test catalog cross validators."""

    stores = setup_stores(store_uri)
    entry = get_test_entry_for_store()

    with ManagedCatalogSession(stores.catalog_stores.session()) as catalog_stores:
        catalog_session = catalog_stores.get_session(SessionStores.LOCAL_CATALOG_STORE_ID)

        # Valid submission
        catalog_session.entry_mapper.create_with_header(entry, VALID_USER)

        # Invalid user submission
        with pytest.raises(RuntimeError):
            catalog_session.entry_mapper.create_with_header(entry, INVALID_USER)
        
        # Invalid quality attribute submission
        entry.quality_attribute = "not a quality attribute"
        with pytest.raises(RuntimeError):
            catalog_session.entry_mapper.create_with_header(entry, INVALID_USER)
