"""A simple measurement class derived from ExternalMeasurement, to import data."""

import json
import typing
from collections.abc import Callable
from typing import Any

from mlte.evidence.artifact import Evidence
from mlte.evidence.types.opaque import Opaque
from mlte.measurement.external_measurement import ExternalMeasurement


class ImportMeasurement(ExternalMeasurement):
    """Simple class derived from ExternalMeasurement that loads data from a JSON file and wraps it in an Opaque evidence type."""

    def __init__(
        self,
        test_case_id: str | None = None,
    ):
        """
        Initialize a new ImportMeasurement measurement.

        :param test_case_id: A unique identifier for the test case associated to this.
        """
        self.output_evidence_type: type = Opaque
        """The output Evidence type that calls to evaluate will return."""

        self.function: Callable[..., Any] | None = _load_json
        """Store the callable function itself."""

        # Call base constructor.
        super().__init__(test_case_id=test_case_id, function=self.function)

    # Overriden.
    def __call__(self, import_path: str) -> Evidence:
        """Evaluate a measurement and return values without semantics."""
        return super().__call__(import_path)


def _load_json(import_path: str) -> dict[str, Any]:
    """Loads a JSON into a dict."""
    with open(import_path, encoding="utf-8") as file:
        data = typing.cast(dict[str, Any], json.load(file))
        return data
