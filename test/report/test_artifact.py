"""
test/report/test_artifact.py

Unit tests for report artifact type.
"""

from typing import Tuple

from mlte.context.context import Context
from mlte.report.artifact import Report
from mlte.store.artifact.store import ArtifactStore
from test.store.artifact.fixture import store_with_context  # noqa


def test_round_trip() -> None:
    """Report can be converted to model and back."""

    report = Report("my-report")

    model = report.to_model()
    _ = Report.from_model(model)


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Report can be saved to and loaded from artifact store."""
    store, ctx = store_with_context

    report = Report("my-report")
    report.save_with(ctx, store)

    loaded = Report.load_with("my-report", context=ctx, store=store)
    assert loaded == report
