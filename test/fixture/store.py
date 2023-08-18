"""
test/fixture/store.py

A simple fixture for an in-memory artifact store.
"""

import pytest

from mlte.context.context import Context
from mlte.context.model import ModelCreate, NamespaceCreate, VersionCreate
from mlte.store.factory import create_store
from mlte.store.base import ManagedSession, Store

# The namespace identifier for default context
FX_NAMESPACE_ID = "ns0"

# The mode identifier for default context
FX_MODEL_ID = "model0"

# The version identifier for default context
FX_VERSION_ID = "v0"


@pytest.fixture(scope="function")
def store_with_context() -> tuple[Store, Context]:
    """Create an in-memory artifact store with initial context."""
    store = create_store("memory://")
    with ManagedSession(store.session()) as handle:
        _ = handle.create_namespace(NamespaceCreate(identifier=FX_NAMESPACE_ID))
        _ = handle.create_model(
            FX_NAMESPACE_ID, ModelCreate(identifier=FX_MODEL_ID)
        )
        _ = handle.create_version(
            FX_NAMESPACE_ID,
            FX_MODEL_ID,
            VersionCreate(identifier=FX_VERSION_ID),
        )

    return store, Context(FX_NAMESPACE_ID, FX_MODEL_ID, FX_VERSION_ID)
