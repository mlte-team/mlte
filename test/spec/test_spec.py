"""
test/spec/test_spec.py

Unit tests for Spec functionality.
"""

from __future__ import annotations

import pytest

from mlte.measurement.storage import LocalObjectSize
from mlte.property.costs import StorageCost
from mlte.spec import Requirement, Spec


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_save(tmp_path):
    s = Spec(
        {
            StorageCost("rationale"): [
                Requirement("test", LocalObjectSize.value().less_than(3))
            ]
        }
    )
    s.save()

    r = Spec.load()
    assert s == r


@pytest.mark.skip("Disabled for artifact protocol development.")
def test_load_failure(tmp_path):
    with pytest.raises(RuntimeError):
        _ = Spec.load()


def test_non_unique_properties():
    with pytest.raises(RuntimeError):
        _ = Spec({StorageCost("rationale"): [], StorageCost("rationale2"): []})


def test_non_unique_requirement_ids():
    requirement1 = Requirement("id1", LocalObjectSize.value().less_than(5))
    requirement2 = Requirement("id1", LocalObjectSize.value().less_than(3))
    with pytest.raises(RuntimeError):
        _ = Spec({StorageCost("rationale"): [requirement1, requirement2]})
