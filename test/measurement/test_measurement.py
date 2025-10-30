"""Unit tests for Measurement."""

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.string import String
from mlte.measurement.measurement import Measurement


class SampleProcessMeasurement(Measurement):
    def __call__(self, first_arg: str, *args, **kwargs) -> Evidence:
        print(first_arg)
        return String(first_arg)

    @classmethod
    def get_output_type(cls) -> type[Evidence]:
        return String


def test_serialize():
    """Test that a Measurement metadata can be properly serialized."""
    test_id = "test"

    # Serialize and deserialize, without group.
    measurement = SampleProcessMeasurement(test_case_id=test_id)
    metadata = measurement.generate_metadata()
    deserialized = SampleProcessMeasurement.from_metadata(metadata, test_id)
    assert deserialized == measurement
