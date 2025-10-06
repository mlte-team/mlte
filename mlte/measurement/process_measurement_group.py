"""Handling multiple process measurements at the same time more easily."""

from typing import Any

from mlte.evidence.artifact import Evidence
from mlte.measurement.process_measurement import ProcessMeasurement


class ProcessMeasurementGroup:
    """
    Class that allows you to run multiple separte ProcessMeasurement classes
    on the same external process with an interface similar to regular Measurements.
    TODO: Change this into an actual Measurement when TestCases can be associated with more
    than one piece of evidence. Currently this can't be used as an automatically executed
    measurement with TestSuite.run_measurements().
    """

    def __init__(self):
        self.measurements: list[ProcessMeasurement] = []
        """List of process measurements to evaluate."""

    def add(self, measurement: ProcessMeasurement) -> None:
        """Add a measurement to the internal list."""
        self.measurements.append(measurement)

    def evaluate(
        self, command: list[str], inputs: dict[str, list[Any]] = {}
    ) -> dict[str, Evidence]:
        """Start an external process and run multiple process measurements on it."""
        # Start the external process to measure.
        pid = ProcessMeasurement.start_process(command[0], command[1:])

        # Start up all measurement tools.
        for measurement in self.measurements:
            if not measurement.evidence_metadata:
                raise RuntimeError(
                    "Can't evaluate measurement before setting its id"
                )
            curr_inputs = (
                inputs[measurement.test_case_id]
                if measurement.test_case_id in inputs
                else []
            )
            measurement.evaluate_async(pid, *curr_inputs)

        # Wait for results. This could be threaded, but not clear if the benefits make it worth it.
        evidences: dict[str, Evidence] = {}
        for measurement in self.measurements:
            if measurement.evidence_metadata:
                evidence = measurement.wait_for_output().with_metadata(
                    measurement.evidence_metadata
                )
                evidences[measurement.evidence_metadata.test_case_id] = evidence

        return evidences
