"""
test/negotiation/test_negotiation_card.py

Unit tests for negotiation card.
"""

import mlte.negotiation as nc

# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


def test_problem_type() -> None:
    p = nc.ProblemType.CLASSIFICATION
    s = p.to_json()
    d = nc.ProblemType.from_json(s)
    assert p == d


def test_metric_descriptor() -> None:
    m = nc.MetricDescriptor()
    m.description = "description"
    m.baseline = "baseline"

    s = m.to_json()
    d = nc.MetricDescriptor.from_json(s)

    assert m == d
