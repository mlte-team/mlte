"""
test/report/test_artifact.py

Unit tests for report artifact type.
"""

from typing import Tuple

from mlte.artifact.type import ArtifactType
from mlte.context.context import Context
from mlte.report.artifact import Report
from mlte.store.artifact.store import ArtifactStore
from test.fixture.artifact import ArtifactModelFactory
from test.store.artifact.fixture import store_with_context  # noqa


def test_round_trip() -> None:
    """Report can be converted to model and back."""

    report = Report.from_model(
        ArtifactModelFactory.make(ArtifactType.REPORT, id="my-report")
    )

    model = report.to_model()
    _ = Report.from_model(model)


def test_save_load(
    store_with_context: Tuple[ArtifactStore, Context]  # noqa
) -> None:
    """Report can be saved to and loaded from artifact store."""
    store, ctx = store_with_context
    initial_id = "my-report"

    report = Report.from_model(
        ArtifactModelFactory.make(ArtifactType.REPORT, id=initial_id)
    )
    report.save_with(ctx, store)

    report_id = report.identifier
    assert report_id != initial_id and report_id.startswith(
        Report.build_full_id(initial_id)
    )

    loaded = Report.load_with(report_id, context=ctx, store=store)
    assert loaded == report
