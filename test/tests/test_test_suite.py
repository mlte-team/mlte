"""
Unit tests for TestSuite functionality.
"""

from __future__ import annotations

from typing import Any, Tuple

import pytest

from mlte.context.context import Context
from mlte.evidence.types.image import Image
from mlte.evidence.types.integer import Integer
from mlte.evidence.types.real import Real
from mlte.measurement.external_measurement import ExternalMeasurement
from mlte.measurement.storage import LocalObjectSize
from mlte.store.artifact.store import ArtifactStore
from mlte.tests.test_case import TestCase
from mlte.tests.test_suite import TestSuite
from test.store.artifact.fixture import store_with_context  # noqa


def get_sample_test_suite():
    test_suite = TestSuite(
        identifier="test_suite",
        test_cases=[
            TestCase(identifier="t1", goal="to test", qas_list=["qa1"])
        ],
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
        test_cases=[TestCase(identifier="t1", goal="to test", qas_list=["qa1"])]
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


def test_repeated_ids():
    """Check that received test cases have unique ids."""
    with pytest.raises(RuntimeError):
        _ = TestSuite(
            test_cases=[
                TestCase(identifier="t1", goal="to test", qas_list=["qa1"]),
                TestCase(identifier="t1", goal="to test", qas_list=["qa1"]),
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
                qas_list=["qas3"],
                validator=LocalObjectSize.output_type().less_than(150000000),
                measurement=LocalObjectSize("model size"),
            ),
            TestCase(
                identifier="overall accuracy",
                goal="Measure the overall accuracy of your end to end pipeline",
                qas_list=["qas8"],
                validator=Real.greater_than(0.9),
                measurement=ExternalMeasurement(
                    "overall accuracy", Real, internal_cal_function
                ),
            ),
            TestCase(
                identifier="image attributions",
                goal="Check what the model is doing",
                qas_list=["qas7"],
                validator=Image.register_info("Inspect the image."),
                measurement=ExternalMeasurement("image attributions", Image),
            ),
            TestCase(
                identifier="no measurement",
                goal="This test has no initial measurement",
                qas_list=["qas8"],
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

    assert type(evidence[0]) is Integer and evidence[0].value > 0
    assert type(evidence[1]) is Real and evidence[1].value == 4.0
    assert type(evidence[2]) is Image and "Image" in str(evidence[2])


def test_run_measurements_invalid_id():
    """Check that invalid ids are properly handled in bulk measurement runs."""

    # Test suite to run measurements on.
    test_suite = TestSuite(
        test_cases=[
            TestCase(
                identifier="model size",
                goal="Check storage consumption",
                qas_list=["qas3"],
                validator=LocalObjectSize.output_type().less_than(150000000),
                measurement=LocalObjectSize("model size"),
            ),
        ]
    )

    inputs: dict[str, list[Any]] = {
        "model sizer": ["./"],
    }

    with pytest.raises(RuntimeError):
        _ = test_suite.run_measurements(input=inputs)
