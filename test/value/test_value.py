"""
mlte/value/test_value.py

Unit tests for Value.
"""

from typing import Tuple

from mlte.context.context import Context
from mlte.evidence.metadata import EvidenceMetadata, Identifier
from mlte.store.artifact.store import ArtifactStore
from mlte.value.artifact import Value
from mlte.value.types.integer import Integer
from mlte.value.types.real import Real

from ..fixture.store import store_with_context  # noqa


def test_load_all(
    store_with_context: Tuple[ArtifactStore, Context],  # noqa
):
    """
    Loading all models of a given type.
    """
    store, ctx = store_with_context

    m1 = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id1")
    )
    v1 = Integer(m1, 10)
    m2 = EvidenceMetadata(
        measurement_type="typename", identifier=Identifier(name="id2")
    )
    v2 = Real(m2, 3.14)
    v1.save_with(ctx, store, parents=True)
    v2.save_with(ctx, store)

    models = Value.load_all_with(ctx, store)

    assert len(models) == 2
    assert models[0] == v1 or models[0] == v2
    assert models[1] == v1 or models[1] == v2
