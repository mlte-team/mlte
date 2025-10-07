"""Handling multiple process measurements at the same time more easily."""

from typing import Any

from mlte.evidence.artifact import Evidence
from mlte.measurement.process_measurement import ProcessMeasurement


class ProcessMeasurementGroup:
    """
    Class that allows you to run multiple separte ProcessMeasurement classes
    on the same external process with an interface similar to regular Measurements.
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
        pid = ProcessMeasurement.start_process(command)

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

    @staticmethod
    def evaluate_groups(
        groups: dict[str, list[ProcessMeasurement]],
        inputs: dict[str, list[Any]],
    ) -> dict[str, Evidence]:
        """
        Given groups of measurements, run each group in a ProcessMeasurementGroup.

        :param groups: A dict of groups keyed by group id, each group having a list of ProcessMeasurements to be run together.
        :param inputs: A dict of inputs, per test case id.
        :returns: A dict of evidences, by test case id.
        """
        all_evidences: dict[str, Evidence] = {}
        for _, group in groups.items():
            # Create a ProcessMeasurementGroup for group.
            measurement_group = ProcessMeasurementGroup()
            for measurement in group:
                # Only consider measurements that have a case id properly set up.
                if measurement.test_case_id:
                    measurement_group.add(measurement)

                    # We assume all test cases in the group have the same command.
                    # TODO: see if we should improve this, or check for this.
                    command = inputs[measurement.test_case_id]

            # Execute command and run all measurements.
            evidences = measurement_group.evaluate(command, inputs)
            all_evidences.update(evidences)

        return all_evidences
