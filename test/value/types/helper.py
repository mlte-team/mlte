from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata


def get_sample_evidence_metadata() -> EvidenceMetadata:
    return EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="typename", output_class="output"
        ),
        test_case_id="id",
    )
