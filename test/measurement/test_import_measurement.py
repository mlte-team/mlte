import json

from mlte.evidence.types.opaque import Opaque
from mlte.measurement.import_measurement import ImportMeasurement


def test_load_valid_json(tmp_path):
    """Test that a valid JSON file is loaded correctly."""
    # Create a valid JSON file in the temporary directory.
    test_path = tmp_path / "test.json"
    expected_data = {"key": "value", "number": 123}
    with open(test_path, "w") as f:
        json.dump(expected_data, f)
    test_case_id = "test_id"

    measurement = ImportMeasurement(test_case_id)
    evidence = measurement.evaluate(test_path)

    assert type(evidence) is Opaque
    assert evidence.data == expected_data
