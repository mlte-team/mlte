"""Handling multiple process measurements at the same time more easily."""

from mlte.evidence.artifact import Evidence
from mlte.measurement.process_measurement import ProcessMeasurement


class ProcessGroupMeasurement:
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
        self, command: str, arguments: list[str], *args, **kwargs
    ) -> list[Evidence]:
        """Start an external process and run multiple process measurements on it."""
        # Start the external process to measure.
        pid = ProcessMeasurement.start_process(command, arguments)

        # Do the measurements.
        return self.__call__(pid, *args, **kwargs)

    def __call__(self, pid: int, *args, **kwargs) -> list[Evidence]:
        """Execute each measurement asynchronously"""
        # Start up all measurement tools.
        for measurement in self.measurements:
            measurement.evaluate_async(pid, *args, **kwargs)

        # Wait for results. This could be threaded, but not sure of the benefits.
        evidences: list[Evidence] = []
        for measurement in self.measurements:
            if not measurement.evidence_metadata:
                raise RuntimeError(
                    "Can't evaluate measurement before setting its id"
                )
            evidence = measurement.wait_for_output().with_metadata(
                measurement.evidence_metadata
            )
            evidences.append(evidence)

        return evidences
