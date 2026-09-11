# ruff: noqa

spec = TestSuite(
    test_cases=[
        TestCase(
            identifier="training_cpu_utilization",
            goal="Check average training CPU utilization",
            quality_scenarios=["card.training_resource_profile-qas_001"],
            measurement=LocalProcessCPUUtilization(),
            validator=CPUStatistics.average_utilization_less_than(80.0),
        ),
        TestCase(
            identifier="training_memory_utilization",
            goal="Check maximum training memory utilization",
            quality_scenarios=["card.training_resource_profile-qas_002"],
            measurement=LocalProcessMemoryUtilization(),
            validator=LocalProcessMemoryUtilization.get_output_type().max_utilization_less_than(
                8.0,
                unit=Units.gigabyte,
            ),
        ),
        TestCase(
            identifier="training_output_bundle_size",
            goal="Check training output bundle size",
            quality_scenarios=["card.training_resource_profile-qas_003"],
            measurement=LocalObjectSize(),
            validator=Real.less_or_equal_to(2.0, unit=Units.gigabyte),
        ),
        # Reviewer: implement validators.training_metadata_complete(...) because imported JSON metadata requires project-specific field checks
        # Testability test case
        TestCase(
            identifier="imported_training_metadata",
            goal="Check imported training metadata completeness",
            quality_scenarios=["card.training_resource_profile-qas_004"],
            measurement=ImportMeasurement(),
            validator=validators.training_metadata_complete(
                required_fields=[
                    "training_duration",
                    "random_seed",
                    "dataset_version",
                    "model_artifact_path",
                ],
            ),
        ),
    ]
)
spec.save(parents=True, force=True)
