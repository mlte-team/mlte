"""
test/negotiation/test_model.py

Unit tests for negotiation card model.
"""

from __future__ import annotations

from typing import Any, Dict

from deepdiff import DeepDiff

from mlte.model.shared import (
    GoalDescriptor,
    MetricDescriptor,
    ProblemType,
    RiskDescriptor,
    SystemDescriptor,
)
from mlte.negotiation.model import NegotiationCardModel
from test.fixture.artifact import make_complete_negotiation_card

# -----------------------------------------------------------------------------
# NegotiationCardModel
# -----------------------------------------------------------------------------


def test_negotiation_card() -> None:
    """A negotiation card model can be serialized and deserialized."""
    objects = [
        make_complete_negotiation_card(),
        NegotiationCardModel(),
    ]

    for object in objects:
        s = object.to_json()
        d = NegotiationCardModel.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# System Subcomponents
# -----------------------------------------------------------------------------


def test_system_descriptor() -> None:
    """A system descriptor model can be serialized and deserialized."""
    objects = [
        SystemDescriptor(
            goals=[
                GoalDescriptor(
                    description="description",
                    metrics=[
                        MetricDescriptor(
                            description="description", baseline="baseline"
                        )
                    ],
                )
            ],
            problem_type=ProblemType.CLASSIFICATION,
            task="task",
            usage_context="usage_context",
            risks=RiskDescriptor(fp="fp", fn="fn", other="other"),
        ),
        SystemDescriptor(),
    ]
    for object in objects:
        s = object.to_json()
        d = SystemDescriptor.from_json(s)
        assert d == object


# -----------------------------------------------------------------------------
# Test Helpers
# -----------------------------------------------------------------------------


def deepequal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    return len(DeepDiff(a, b)) == 0
