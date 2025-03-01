"""
Unit tests for TestSuite functionality.
"""

from __future__ import annotations

from typing import Tuple

import pytest

from mlte.context.context import Context
from mlte.spec.test_case import TestCase
from mlte.spec.test_suite import TestSuite
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa


def get_sample_test_suite():
    test_suite = TestSuite(
        identifier="test_suite",
        test_cases={
            "t1": TestCase(identifier="t1", goal="to test", qas_list=["qa1"])
        },
    )
    return test_suite


def test_round_trip() -> None:
    """TestSuite can be converted to model and back."""
    test_suite = get_sample_test_suite()

    model = test_suite.to_model()
    loaded = TestSuite.from_model(model)

    assert test_suite == loaded


def test_save_load(store_with_context: Tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context
    test_suite = get_sample_test_suite()

    test_suite.save_with(ctx, store)
    loaded = TestSuite.load_with("test_suite", context=ctx, store=store)

    assert test_suite == loaded


def test_save_load_default(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context

    test_suite = TestSuite(
        test_cases={
            "t1": TestCase(identifier="t1", goal="to test", qas_list=["qa1"])
        },
    )
    test_suite.save_with(ctx, store)

    loaded = TestSuite.load_with(context=ctx, store=store)
    assert test_suite == loaded


def test_load_failure(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
):
    store, ctx = store_with_context
    with pytest.raises(RuntimeError):
        _ = TestSuite.load_with("test_suite", context=ctx, store=store)
