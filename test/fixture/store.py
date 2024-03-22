"""
test/fixture/store.py

A simple fixture for an in-memory artifact store.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.context.model import ModelCreate, VersionCreate
from mlte.store.artifact.factory import create_store
from mlte.store.artifact.store import ArtifactStore, ManagedArtifactSession
from mlte.store.base import StoreURIPrefix

# The mode identifier for default context
FX_MODEL_ID = "model0"

# The version identifier for default context
FX_VERSION_ID = "v0"


@pytest.fixture(scope="function")
def store() -> ArtifactStore:
    """Create an in-memory artifact store."""
    return create_store(StoreURIPrefix.LOCAL_MEMORY[0])


@pytest.fixture(scope="function")
def store_with_context() -> Tuple[ArtifactStore, Context]:
    """Create an in-memory artifact store with initial context."""
    store = create_store(StoreURIPrefix.LOCAL_MEMORY[0])
    with ManagedArtifactSession(store.session()) as handle:
        _ = handle.create_model(ModelCreate(identifier=FX_MODEL_ID))
        _ = handle.create_version(
            FX_MODEL_ID,
            VersionCreate(identifier=FX_VERSION_ID),
        )

    return store, Context(FX_MODEL_ID, FX_VERSION_ID)
