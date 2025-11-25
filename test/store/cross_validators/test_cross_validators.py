"""Unit tests for CrossValidator functionality."""

from pathlib import Path
from unittest.mock import patch
import pytest
import sqlalchemy

from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.session.session_stores import SessionStores, setup_stores
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.base import StoreType, StoreURI
from mlte.store.catalog.catalog_group import ManagedCatalogGroupSession
from test.fixture.artifact import ArtifactModelFactory
from test.store.artifact.test_underlying import check_artifact_writing
from test.store.catalog.fixture import get_test_entry_for_store

from test.store.defaults import IN_MEMORY_SQLITE_DB

CACHED_IN_MEMORY_SQLITE_DB = IN_MEMORY_SQLITE_DB + "?cache=shared&mode=memory"
URIS = ["memory://", "fs://", CACHED_IN_MEMORY_SQLITE_DB]
MODEL_ID = "model0"
VERISON_ID = "version0"
ARTIFACT_ID = "myid"
VALID_USER = "admin"
INVALID_USER = "not a user"

# HTTP wasn't working, and rdbs isn't seeing custom_list entry table


@pytest.fixture(scope="function")
def shared_sqlite_engine():
    """Opens a connection to a shared in-memory DB and keeps it alive."""
    engine = sqlalchemy.create_engine(CACHED_IN_MEMORY_SQLITE_DB)
    engine.dispose = lambda: None
    yield engine
    engine.dispose()


@pytest.mark.parametrize("store_uri", URIS)
def test_artifact_cross_validators(store_uri: str, tmp_path: Path, shared_sqlite_engine):
    """Test artifact cross validators."""

    if StoreURI.from_string(store_uri).type == StoreType.LOCAL_FILESYSTEM:
        store_uri += str(tmp_path)

    if store_uri == CACHED_IN_MEMORY_SQLITE_DB:
        with patch("mlte.store.common.rdbs_storage.sqlalchemy.create_engine") as mock_create_engine:
            mock_create_engine.return_value = shared_sqlite_engine
            stores = setup_stores(store_uri)
    else:
        stores = setup_stores(store_uri)

    with ManagedArtifactSession(
        stores.artifact_store.session()
    ) as artifact_store:
        artifact_store.model_mapper.create(Model(identifier=MODEL_ID))
        artifact_store.version_mapper.create(
            Version(identifier=VERISON_ID), MODEL_ID
        )

        artifact = ArtifactModelFactory.make(
            ArtifactType.NEGOTIATION_CARD, ARTIFACT_ID
        )
        artifact_id = artifact.header.identifier

        # Valid submission
        _ = check_artifact_writing(
            artifact_store,
            MODEL_ID,
            VERISON_ID,
            artifact_id,
            artifact,
            VALID_USER,
        )

        # Invalid user submission
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store,
                MODEL_ID,
                VERISON_ID,
                artifact_id,
                artifact,
                INVALID_USER,
            )

        # Invalid quality attribute submission
        artifact.body.system_requirements[0].quality = "not a quality attribute"
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store,
                MODEL_ID,
                VERISON_ID,
                artifact_id,
                artifact,
                VALID_USER,
            )

    # TODO: make sure this is create and edit


@pytest.mark.parametrize("store_uri", URIS)
def test_catalog_cross_validators(store_uri: str, tmp_path: Path, shared_sqlite_engine):
    """Test catalog cross validators."""

    if StoreURI.from_string(store_uri).type == StoreType.LOCAL_FILESYSTEM:
        store_uri += str(tmp_path)

    if store_uri == CACHED_IN_MEMORY_SQLITE_DB:
        with patch("mlte.store.common.rdbs_storage.sqlalchemy.create_engine") as mock_create_engine:
            mock_create_engine.return_value = shared_sqlite_engine
            stores = setup_stores(store_uri)
    else:
        stores = setup_stores(store_uri)
    
    entry = get_test_entry_for_store()

    with ManagedCatalogGroupSession(
        stores.catalog_stores.session()
    ) as group_session:
        local_catalog_session = group_session.sessions[SessionStores.LOCAL_CATALOG_STORE_ID]

        # Valid submission
        _ = local_catalog_session.entry_mapper.create_with_header(entry, VALID_USER)

        # Invalid user submission
        with pytest.raises(RuntimeError):
            local_catalog_session.entry_mapper.create_with_header(entry, INVALID_USER)

        # Invalid quality attribute submission
        entry.quality_attribute = "not a quality attribute"
        with pytest.raises(RuntimeError):
            local_catalog_session.entry_mapper.create_with_header(entry, INVALID_USER)
