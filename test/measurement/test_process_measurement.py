"""Unit tests for ProcessMeasurement."""

import os

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.string import String
from mlte.measurement.process_measurement import ProcessMeasurement
from mlte.measurement.process_measurement_group import ProcessMeasurementGroup
from test.support.meta import path_to_support

# The spin duration, in seconds
SPIN_DURATION = 1
SPIN_COMMAND = [
    "python3",
    os.path.join(path_to_support(), "spin.py"),
    str(SPIN_DURATION),
]


class SampleProcessMeasurement(ProcessMeasurement):
    def __call__(self, pid: int, first_arg: str, *args, **kwargs) -> Evidence:
        print(first_arg)
        return String(first_arg)

    @classmethod
    def get_output_type(cls) -> type[Evidence]:
        return String


def test_start_script_job():
    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_script(SPIN_COMMAND[1:])

    assert pid > 0


def test_start_general_job():
    # Spawn external job; blocks until process exit
    pid = ProcessMeasurement.start_process(SPIN_COMMAND)

    assert pid > 0


def test_serialize():
    """Test that a ProcessMeasurement metadata can be properly serialized."""
    test_id = "test"

    measurement = SampleProcessMeasurement(test_case_id=test_id, group="group1")
    metadata = measurement.generate_metadata()
    deserialized = SampleProcessMeasurement.from_metadata(metadata, test_id)

    assert deserialized == measurement


def test_evaluate_sync() -> None:
    """Test that we can properly evaluate synchronously."""
    m = SampleProcessMeasurement("id1")

    result = m.evaluate(SPIN_COMMAND, "test")

    assert type(result) is String and result.value == "test"
    assert m.evidence_metadata and m.evidence_metadata.test_case_id == "id1"


def test_evaluate_async() -> None:
    """Test that we can properly evaluate asynchronously."""
    m = SampleProcessMeasurement("id1")

    pid = ProcessMeasurement.start_process(SPIN_COMMAND)

    m.evaluate_async(pid, "test")
    result = m.wait_for_output()

    assert type(result) is String and result.value == "test"
    assert m.evidence_metadata and m.evidence_metadata.test_case_id == "id1"


def test_process_measurement_group_evaluate():
    """Tests that group measurement works."""

    # Create measurement group
    measurements = ProcessMeasurementGroup()

    # Add measurements to group.
    measurements.add(SampleProcessMeasurement("t1"))
    measurements.add(SampleProcessMeasurement("t2"))

    # Evaluate the measurements.
    evidences = measurements.evaluate(
        command=SPIN_COMMAND,
        inputs={"t1": [SPIN_COMMAND, "test"], "t2": [SPIN_COMMAND, "test2"]},
    )

    assert type(evidences["t1"]) is String and evidences["t1"].value == "test"
    assert type(evidences["t2"]) is String and evidences["t2"].value == "test2"
    assert (
        evidences["t1"].metadata
        and evidences["t1"].metadata.test_case_id == "t1"
    )
    assert (
        evidences["t2"].metadata
        and evidences["t2"].metadata.test_case_id == "t2"
    )


def test_process_measurement_group_groups():
    """Tests that group measurement works."""

    # Set up groups.
    groups: dict[str, list[ProcessMeasurement]] = {
        "group1": [
            SampleProcessMeasurement("t1", group="group1"),
            SampleProcessMeasurement("t2", group="group1"),
        ],
        "group2": [
            SampleProcessMeasurement("t3", group="group2"),
            SampleProcessMeasurement("t4", group="group2"),
        ],
    }

    # Evaluate the measurements.
    evidences = ProcessMeasurementGroup.evaluate_groups(
        groups=groups,
        inputs={
            "t1": [SPIN_COMMAND, "test"],
            "t2": [SPIN_COMMAND, "test2"],
            "t3": [SPIN_COMMAND, "test3"],
            "t4": [SPIN_COMMAND, "test4"],
        },
    )

    assert type(evidences["t1"]) is String and evidences["t1"].value == "test"
    assert type(evidences["t2"]) is String and evidences["t2"].value == "test2"
    assert type(evidences["t3"]) is String and evidences["t3"].value == "test3"
    assert type(evidences["t4"]) is String and evidences["t4"].value == "test4"
    assert (
        evidences["t1"].metadata
        and evidences["t1"].metadata.test_case_id == "t1"
    )
    assert (
        evidences["t2"].metadata
        and evidences["t2"].metadata.test_case_id == "t2"
    )
    assert (
        evidences["t3"].metadata
        and evidences["t3"].metadata.test_case_id == "t3"
    )
    assert (
        evidences["t4"].metadata
        and evidences["t4"].metadata.test_case_id == "t4"
    )
