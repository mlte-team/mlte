"""
test/session/test_session.py

Unit tests for global session management.
"""

import pytest

from mlte.session import session, set_context, set_store
from mlte.store.artifact.store import ArtifactStore
from mlte.store.base import StoreURIPrefix

from ..store.artifact.fixture import (  # noqa
    fs_store,
    http_store,
    memory_store,
    rdbs_store,
    stores,
)


def test_session() -> None:
    model = "model"
    version = "v0.0.1"
    uri = StoreURIPrefix.LOCAL_MEMORY[0]

    set_context(model, version)
    set_store(uri)

    s = session()

    assert s.context.model == model
    assert s.context.version == version
    assert s.store.uri.uri == uri


@pytest.mark.parametrize("store_fixture_name", stores())
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

    assert s.store.session().read_model(model).identifier == model
    assert s.store.session().read_version(model, version).identifier == version
