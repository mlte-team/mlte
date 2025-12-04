"""Unit tests for TestSuite functionality."""

from __future__ import annotations

import typing
from typing import Any, Optional

import pytest

from mlte.context.context import Context
from mlte.evidence.types.image import Image
from mlte.evidence.types.real import Real
from mlte.measurement.external_measurement import ExternalMeasurement
from mlte.measurement.storage import LocalObjectSize
from mlte.negotiation.artifact import NegotiationCard
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.test_case import TestCase
from mlte.tests.test_suite import TestSuite
from test.negotiation.test_artifact import get_sample_negotiation_card
from test.store.artifact.fixture import store_with_context  # noqa


def get_sample_test_suite(
    identifier: Optional[str] = None, qas_ids: list[str] = []
):
    test_suite = TestSuite(
        identifier=identifier if identifier else "test_suite",
        test_cases=[
            TestCase(
                identifier="model size",
                goal="Check storage consumption",
                quality_scenarios=qas_ids,
                validator=LocalObjectSize.get_output_type().less_than(
                    150000000
                ),
                measurement=LocalObjectSize("model size"),
            ),
        ],
    )
    return test_suite


def test_round_trip() -> None:
    """TestSuite can be converted to model and back."""
    test_suite = get_sample_test_suite()

    model = test_suite.to_model()
    loaded = TestSuite.from_model(model)

    assert test_suite == loaded


def test_save_load(store_with_context: tuple[ArtifactStore, Context]):  # noqa
    store, ctx = store_with_context

    # Setup dependent card with QAS ids.
    card = get_sample_negotiation_card()
    card.save_with(ctx, store)
    card = typing.cast(
        NegotiationCard,
        NegotiationCard.load_with(card.identifier, context=ctx, store=store),
    )
    qas_ids = [scenario.identifier for scenario in card.quality_scenarios]

    id = "test_suite"
    test_suite = get_sample_test_suite(identifier=id, qas_ids=qas_ids)

    test_suite.save_with(ctx, store)
    loaded = TestSuite.load_with(id, context=ctx, store=store)

    assert test_suite == loaded


def test_save_load_default(
    store_with_context: tuple[ArtifactStore, Context],  # noqa
):
    store, ctx = store_with_context
    test_suite = get_sample_test_suite(identifier=TestSuite.build_full_id())

    test_suite.save_with(ctx, store)

    loaded = TestSuite.load_with(context=ctx, store=store)
    assert test_suite == loaded


def test_save_invalid_qasids():
    """Tests if a TestSuite is given a qas id for a scenario that is in no existing NegotiationCard, save will fail."""
    test_suite = get_sample_test_suite(qas_ids=["qas1"])

    with pytest.raises(RuntimeError):
        test_suite.save()


def test_load_failure(
    store_with_context: tuple[ArtifactStore, Context],  # noqa
):
    """Fail to load a suite that doesn't exist."""
    store, ctx = store_with_context
    with pytest.raises(RuntimeError):
        _ = TestSuite.load_with("test_suite", context=ctx, store=store)


def test_repeated_ids():
    """Check that received test cases have unique ids."""
    with pytest.raises(RuntimeError):
        _ = TestSuite(
            test_cases=[
                TestCase(
                    identifier="t1", goal="to test", quality_scenarios=["qa1"]
                ),
                TestCase(
                    identifier="t1", goal="to test", quality_scenarios=["qa1"]
                ),
            ]
        )


def test_run_measurements():
    """Check that we can run bulk measurements."""

    def internal_cal_function(nums: list[float]) -> float:
        """Internal function to simulate call to External measurement"""
        return sum(nums) / len(nums)

    # Test suite to run measurements on.
    test_suite = TestSuite(
        test_cases=[
            TestCase(
                identifier="model size",
                goal="Check storage consumption",
                quality_scenarios=["qas3"],
                validator=LocalObjectSize.get_output_type().less_than(
                    150000000
                ),
                measurement=LocalObjectSize(),
            ),
            TestCase(
                identifier="overall accuracy",
                goal="Measure the overall accuracy of your end to end pipeline",
                quality_scenarios=["qas8"],
                validator=Real.greater_than(0.9),
                measurement=ExternalMeasurement(
                    output_evidence_type=Real, function=internal_cal_function
                ),
            ),
            TestCase(
                identifier="image attributions",
                goal="Check what the model is doing",
                quality_scenarios=["qas7"],
                validator=Image.register_info("Inspect the image."),
                measurement=ExternalMeasurement(output_evidence_type=Image),
            ),
            TestCase(
                identifier="no measurement",
                goal="This test has no initial measurement",
                quality_scenarios=["qas8"],
                validator=Real.greater_than(0.9),
            ),
        ]
    )

    inputs: dict[str, list[Any]] = {
        "model size": ["./"],
        "overall accuracy": [[3, 4, 5]],
        "image attributions": ["test/evidence/types/flower3.jpg"],
    }

    evidence = test_suite.run_measurements(input=inputs)

    assert len(evidence) == 3
    assert (
        type(evidence["model size"]) is Real
        and evidence["model size"].value > 0
    )
    assert (
        type(evidence["overall accuracy"]) is Real
        and evidence["overall accuracy"].value == 4.0
    )
    assert type(evidence["image attributions"]) is Image and "Image" in str(
        evidence["image attributions"]
    )


def test_run_measurements_invalid_id():
    """Check that invalid ids are properly handled in bulk measurement runs."""

    # Test suite to run measurements on.
    test_suite = TestSuite(
        test_cases=[
            TestCase(
                identifier="model size",
                goal="Check storage consumption",
                quality_scenarios=["qas3"],
                validator=LocalObjectSize.get_output_type().less_than(
                    150000000
                ),
                measurement=LocalObjectSize("model size"),
            ),
        ]
    )

    inputs: dict[str, list[Any]] = {
        "model sizer": ["./"],
    }

    with pytest.raises(RuntimeError):
        _ = test_suite.run_measurements(input=inputs)
