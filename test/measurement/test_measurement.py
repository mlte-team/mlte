"""Unit tests for Measurement."""

import pytest

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.string import String
from mlte.evidence.unavailable import Unavailable
from mlte.measurement.measurement import Measurement


class SampleProcessMeasurement(Measurement):
    def __call__(self, first_arg: str, *args, **kwargs) -> Evidence:
        print(first_arg)
        return String(first_arg)

    @classmethod
    def output(cls) -> type[Evidence]:
        return String


class BrokenMeasurement(Measurement):
    def __call__(self, first_arg: str, *args, **kwargs) -> Evidence:
        raise RuntimeError("ERRROR!!!")

    @classmethod
    def output(cls) -> type[Evidence]:
        return String


def test_serialize():
    """Test that a Measurement metadata can be properly serialized."""
    test_id = "test"

    # Serialize and deserialize, without group.
    measurement = SampleProcessMeasurement(test_case_id=test_id)
    metadata = measurement.generate_metadata()
    deserialized = SampleProcessMeasurement.from_metadata(metadata, test_id)
    assert deserialized == measurement


def test_force_stop():
    """Tests if the force stop param works as expected."""
    test_id = "test"

    # Serialize and deserialize, without group.
    measurement = BrokenMeasurement(test_case_id=test_id)

    measurement.force_stop = True
    with pytest.raises(RuntimeError):
        measurement.evaluate("test")

    measurement.force_stop = False
    evidence = measurement.evaluate("test")
    assert type(evidence) is Unavailable
    assert evidence.details == "ERRROR!!!"
