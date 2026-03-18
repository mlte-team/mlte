"""Unit tests for CrossValidator functionality."""

import typing
from pathlib import Path

import pytest

from mlte.artifact.type import ArtifactType
from mlte.context.model import Model, Version
from mlte.negotiation.model import NegotiationCardModel
from mlte.session.unified_store import UnifiedStore
from mlte.store.artifact.store_session import ManagedArtifactSession
from mlte.store.base import StoreType
from mlte.store.catalog.catalog_group import ManagedCatalogGroupSession
from test.fixture.artifact import ArtifactModelFactory
from test.session.conftest import create_test_session_stores
from test.store.artifact.test_underlying import check_artifact_writing
from test.store.catalog.conftest import get_test_entry_for_store
from test.store.utils import store_types

MODEL_ID = "model0"
VERISON_ID = "version0"
ARTIFACT_ID = "myid"
VALID_USER = "admin"
INVALID_USER = "not a user"


@pytest.mark.parametrize("store_type", store_types())
def test_artifact_cross_validators(
    store_type: StoreType, tmp_path: Path, patched_setup_stores
) -> None:
    """Test artifact cross validators."""

    stores = create_test_session_stores(
        store_type, tmp_path, patched_setup_stores
    )

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
        body = typing.cast(NegotiationCardModel, artifact.body)
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

        # Invalid problem type submission
        valid_problem_type = body.system.problem_type
        body.system.problem_type = "not a problem type"
        artifact.body = body
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store,
                MODEL_ID,
                VERISON_ID,
                artifact_id,
                artifact,
                VALID_USER,
            )
        body.system.problem_type = valid_problem_type
        artifact.body = body

        # Invalid classification submission
        valid_classification = body.data[0].classification
        body.data[0].classification = "not a classification"
        artifact.body = body
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store,
                MODEL_ID,
                VERISON_ID,
                artifact_id,
                artifact,
                VALID_USER,
            )
        body.data[0].classification = valid_classification
        artifact.body = body

        # Invalid quality attribute submission
        body.system_requirements[0].quality = "not a quality attribute"
        artifact.body = body
        with pytest.raises(RuntimeError):
            _ = check_artifact_writing(
                artifact_store,
                MODEL_ID,
                VERISON_ID,
                artifact_id,
                artifact,
                VALID_USER,
            )


@pytest.mark.parametrize("store_type", store_types())
def test_catalog_cross_validators(
    store_type: StoreType, tmp_path: Path, patched_setup_stores
) -> None:
    """Test catalog cross validators."""

    stores = create_test_session_stores(
        store_type, tmp_path, patched_setup_stores
    )

    entry = get_test_entry_for_store(store_type)

    with ManagedCatalogGroupSession(
        stores.catalog_stores.session()
    ) as group_session:
        local_catalog_session = group_session.sessions[
            UnifiedStore.LOCAL_CATALOG_STORE_ID
        ]

        # Valid submission
        _ = local_catalog_session.entry_mapper.create_with_header(
            entry, user=VALID_USER
        )

        # Invalid user submission
        with pytest.raises(RuntimeError):
            local_catalog_session.entry_mapper.create_with_header(
                entry, user=INVALID_USER
            )

        # Invalid tag submission
        entry.tags.append("not a tag")
        with pytest.raises(RuntimeError):
            local_catalog_session.entry_mapper.create_with_header(
                entry, user=VALID_USER
            )
        entry.tags.pop()

        # Invalid quality attribute submission
        entry.quality_attribute = "not a quality attribute"
        with pytest.raises(RuntimeError):
            local_catalog_session.entry_mapper.create_with_header(
                entry, user=VALID_USER
            )
