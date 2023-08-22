"""
test/spec/test_spec.py

Unit tests for Spec functionality.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.measurement.storage import LocalObjectSize
from mlte.property.costs import StorageCost
from mlte.property.functionality import TaskEfficacy
from mlte.spec.spec import Spec
from mlte.store.base import Store

from ..fixture.store import store_with_context  # noqa


def test_save_load(store_with_context: Tuple[Store, Context]):  # noqa
    store, ctx = store_with_context

    s = Spec(
        "spec",
        {
            StorageCost("rationale"): {
                "test": LocalObjectSize.value().less_than(3)
            }
        },
    )
    s.save_with(ctx, store)

    loaded = Spec.load_with("spec", ctx, store)
    assert s == loaded


def test_load_failure(store_with_context: Tuple[Store, Context]):  # noqa
    store, ctx = store_with_context
    with pytest.raises(RuntimeError):
        _ = Spec.load_with("spec", ctx, store)


def test_non_unique_properties():
    with pytest.raises(RuntimeError):
        _ = Spec(
            "spec",
            {StorageCost("rationale"): {}, StorageCost("rationale2"): {}},
        )


def test_non_unique_requirement_ids():
    with pytest.raises(RuntimeError):
        _ = Spec(
            "spec",
            {
                StorageCost("rationale"): {
                    "id1": LocalObjectSize.value().less_than(5)
                },
                TaskEfficacy("rationale"): {
                    "id1": LocalObjectSize.value().less_than(3),
                },
            },
        )
