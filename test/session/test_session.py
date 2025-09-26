"""Unit tests for global session management."""

import os

import pytest

from mlte.session import session, set_context, set_store
from mlte.session.session import Session, add_catalog_store, reset_session
from mlte.store.artifact.store import ArtifactStore
from mlte.store.base import StoreType, StoreURI

from ..store.artifact.fixture import (  # noqa
    artifact_stores,
    fs_store,
    http_store,
    memory_store,
    rdbs_store,
)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Reset session for each test.
    reset_session()
    yield


def test_session() -> None:
    model = "model"
    version = "v0.0.1"
    cat_id = "test_cat"
    store_uri = StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)
    catalog_store_uri = StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)

    set_context(model, version)
    set_store(store_uri)
    add_catalog_store(catalog_store_uri, cat_id)

    s = session()

    assert s.context.model == model
    assert s.context.version == version
    assert s.stores.artifact_store.uri.uri == store_uri
    assert s.stores.custom_list_store.uri.uri == store_uri
    assert s.stores.catalog_stores.catalogs[cat_id].uri.uri == catalog_store_uri


@pytest.mark.parametrize("store_fixture_name", artifact_stores())
def test_eager_context_creation(
    store_fixture_name: str, request: pytest.FixtureRequest
) -> None:
    # Ignore http_store for now, weird issue setting it up.
    print(store_fixture_name)
    if store_fixture_name == "http_store":
        return

    model = "model"
    version = "v0.0.1"
    store: ArtifactStore = request.getfixturevalue(store_fixture_name)

    set_store(store.uri.uri)
    set_context(model, version, lazy=False)

    s = session()

    assert (
        s.stores.artifact_store.session().read_model(model).identifier == model
    )
    assert (
        s.stores.artifact_store.session()
        .read_version(model, version)
        .identifier
        == version
    )


def test_environment_vars():
    model = "model"
    version = "v0.0.1"
    store_uri = StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)

    os.environ[Session.ENV_CONTEXT_MODEL_VAR] = model
    os.environ[Session.ENV_CONTEXT_VERSION_VAR] = version
    os.environ[Session.ENV_STORE_URI_VAR] = store_uri

    s = session()

    assert s.context.model == model
    assert s.context.version == version
    assert s.stores.artifact_store.uri.uri == store_uri
    assert s.stores.custom_list_store.uri.uri == store_uri

    del os.environ[Session.ENV_CONTEXT_MODEL_VAR]
    del os.environ[Session.ENV_CONTEXT_VERSION_VAR]
    del os.environ[Session.ENV_STORE_URI_VAR]


def test_no_context_setup():
    store_uri = StoreURI.create_uri_string(StoreType.LOCAL_MEMORY)

    set_store(store_uri)

    s = session()

    with pytest.raises(RuntimeError):
        _ = s.context
        _ = s.stores.custom_list_store


def test_no_store_setup():
    model = "model"
    version = "v0.0.1"

    with pytest.raises(RuntimeError):
        set_context(model, version)

        s = session()

        _ = s.stores.artifact_store
        _ = s.stores.custom_list_store
