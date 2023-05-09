"""
Unit tests for Spec functionality.
"""
from __future__ import annotations

import pytest

import mlte
from mlte.spec import Spec, Requirement
from mlte.property.costs import StorageCost
from mlte.measurement import ExternalMeasurement
from mlte.validation import Result


def test_save(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    s = Spec(
        {
            StorageCost("rationale"): [
                Requirement(
                    "test", ExternalMeasurement.__name__, "less_than", 3
                )
            ]
        }
    )
    s.save()

    r = Spec.load()
    assert s == r


def test_load_failure(tmp_path):
    mlte.set_model("model", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{tmp_path}")

    with pytest.raises(RuntimeError):
        _ = Spec.load()


def test_unique_properties():
    with pytest.raises(RuntimeError):
        _ = Spec({StorageCost("rationale"): [], StorageCost("rationale2"): []})


def test_add_requirement():
    spec = Spec({StorageCost("rationale"): []})
    requirement = Requirement(
        "test", ExternalMeasurement.__name__, "less_than", 3
    )
    spec._add_requirement("StorageCost", requirement)

    assert spec.requirements["StorageCost"][0] == Requirement(
        "test", ExternalMeasurement.__name__, "less_than", 3
    )


def test_no_result():
    # Spec validator does not have value for requirement.
    spec = Spec(
        {
            StorageCost("rationale"): [
                Requirement(
                    "test", ExternalMeasurement.__name__, "less_than", 3
                )
            ]
        }
    )

    results: dict[str, dict[str, Result]] = {}
    with pytest.raises(RuntimeError):
        _ = spec.generate_bound_spec(results)
