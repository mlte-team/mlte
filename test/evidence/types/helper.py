from mlte.evidence.metadata import EvidenceMetadata
from mlte.measurement.model import MeasurementMetadata


def get_sample_evidence_metadata(
    test_case_id: str = "test_id",
) -> EvidenceMetadata:
    return EvidenceMetadata(
        measurement=MeasurementMetadata(
            measurement_class="typename", output_class="output"
        ),
        test_case_id=test_case_id,
    )
