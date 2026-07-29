spec = TestSuite(
    test_cases=[
        TestCase(
            identifier="classification_accuracy",
            goal="Check classification accuracy",
            quality_scenarios=["card.classification_evaluation_profile-qas_001"],
            measurement=ExternalMeasurement(
                output_evidence_type=Real,
                function=model.accuracy,
            ),
            validator=Real.greater_or_equal_to(0.90),
        ),
        # Reviewer: implement validators.confusion_matrix_review(...) because class level error patterns require project specific review
        # Analyzability test case
        TestCase(
            identifier="classification_confusion_matrix",
            goal="Check classification confusion matrix",
            quality_scenarios=["card.classification_evaluation_profile-qas_002"],
            measurement=ExternalMeasurement(
                output_evidence_type=Array,
                function=model.confusion_matrix,
            ),
            validator=validators.confusion_matrix_review(),
        ),
        # Reviewer: implement validators.evaluation_summary_metadata_complete(...) because imported JSON metadata requires project specific field checks
        # Testability test case
        TestCase(
            identifier="imported_evaluation_summary",
            goal="Check imported evaluation summary metadata",
            quality_scenarios=["card.classification_evaluation_profile-qas_003"],
            measurement=ImportMeasurement(),
            validator=validators.evaluation_summary_metadata_complete(
                required_fields=[
                    "dataset_identifier",
                    "model_version",
                    "evaluation_timestamp",
                    "evaluator_name",
                ],
            ),
        ),
    ]
)
spec.save(parents=True, force=True)