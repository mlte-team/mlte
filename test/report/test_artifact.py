"""
test/report/test_artifact.py

Unit tests for report artifact type.
"""

from typing import Tuple

from mlte.context.context import Context
from mlte.model.shared import ProblemType
from mlte.negotiation.artifact import NegotiationCard
from mlte.report.artifact import Report
from mlte.report.model import SummaryDescriptor
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


# TODO(Kyle): Exhaustive testing is required here.
def test_populate_from() -> None:
    """The content of a report can be populated from negotiation card."""

    report = Report(
        "my-report",
        summary=SummaryDescriptor(problem_type=ProblemType.BENCHMARKING),
    )

    card = NegotiationCard("my-card")
    card.system.problem_type = ProblemType.CLASSIFICATION

    new = report.populate_from(card)

    assert new.summary.problem_type == ProblemType.CLASSIFICATION
    assert report.summary.problem_type == ProblemType.BENCHMARKING
