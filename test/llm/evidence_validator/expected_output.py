# mypy: ignore-errors
# ruff: noqa: F821
spec = TestSuite(
    test_cases=[
        TestCase(
            identifier="invalid_input_status",
            goal="Check invalid input handling",
            quality_scenarios=["card.evidence_validator_profile-qas_001"],
            validator=String.equal_to("INVALID_INPUT"),
        ),
        TestCase(
            identifier="input_validation_log",
            goal="Check diagnostic logging",
            quality_scenarios=["card.evidence_validator_profile-qas_002"],
            validator=String.contains("Model - Input Validation Error"),
        ),
        TestCase(
            identifier="explanation_image_review",
            goal="Human interpretation of model results",
            quality_scenarios=["card.evidence_validator_profile-qas_003"],
            validator=Image.register_info(
                "Review explanation image evidence for regions used by the model"
            ),
        ),
        TestCase(
            identifier="class_error_pattern_review",
            goal="Human interpretation of model results",
            quality_scenarios=["card.evidence_validator_profile-qas_004"],
            validator=Image.register_info(
                "Review structured class-level error evidence"
            ),
        ),
    ]
)
spec.save(parents=True, force=True)