"""
test/spec/test_spec.py

Unit tests for Spec functionality.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.measurement.storage import LocalObjectSize
from mlte.property.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.store.artifact.store import ArtifactStore
from test.spec.extended_property import ExtendedProperty
from test.store.artifact.fixture import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    s = Spec(
        identifier="spec",
        properties={
            StorageCost("rationale"): {
                "test": LocalObjectSize.value().less_than(3)
            }
        },
    )
    s.save_with(ctx, store)

    loaded = Spec.load_with("spec", context=ctx, store=store)
    assert s == loaded


def test_save_load_default(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context

    s = Spec(
        properties={
            StorageCost("rationale"): {
                "test": LocalObjectSize.value().less_than(3)
            }
        },
    )
    s.save_with(ctx, store)

    loaded = Spec.load_with(context=ctx, store=store)
    assert s == loaded


def test_load_failure(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context
    with pytest.raises(RuntimeError):
        _ = Spec.load_with("spec", context=ctx, store=store)


def test_non_unique_properties():
    with pytest.raises(RuntimeError):
        _ = Spec(
            properties={
                StorageCost("rationale"): {},
                StorageCost("rationale2"): {},
            },
        )


def test_save_load_extended_property(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context

    s = Spec(
        properties={
            ExtendedProperty("rationale"): {
                "test": LocalObjectSize.value().less_than(3)
            }
        },
    )
    s.save_with(ctx, store)

    loaded = Spec.load_with(context=ctx, store=store)
    assert s == loaded
