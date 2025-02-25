"""
test/spec/test_spec.py

Unit tests for Spec functionality.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.measurement.storage import LocalObjectSize
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.spec.spec import Spec
from mlte.store.artifact.store import ArtifactStore
from test.spec.extended_qa_category import ExtendedQACategory
from test.store.artifact.fixture import store_with_context  # noqa


def test_round_trip() -> None:
    """Condition can be converted to model and back."""

    spec = Spec(
        identifier="spec",
        qa_categories={
            StorageCost("rationale"): {
                "test": LocalObjectSize.output_evidence().less_than(3)
            }
        },
    )

    model = spec.to_model()
    loaded = Spec.from_model(model)

    assert spec == loaded


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    s = Spec(
        identifier="spec",
        qa_categories={
            StorageCost("rationale"): {
                "test": LocalObjectSize.output_evidence().less_than(3)
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
        qa_categories={
            StorageCost("rationale"): {
                "test": LocalObjectSize.output_evidence().less_than(3)
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


def test_non_unique_qa_categories():
    with pytest.raises(RuntimeError):
        _ = Spec(
            qa_categories={
                StorageCost("rationale"): {},
                StorageCost("rationale2"): {},
            },
        )


def test_save_load_extended_qa_category(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context

    s = Spec(
        qa_categories={
            ExtendedQACategory("rationale"): {
                "test": LocalObjectSize.output_evidence().less_than(3)
            }
        },
    )
    s.save_with(ctx, store)

    loaded = Spec.load_with(context=ctx, store=store)
    assert s == loaded
