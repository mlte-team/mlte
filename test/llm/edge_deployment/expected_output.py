spec = TestSuite(
    test_cases=[
        TestCase(
            identifier="local_model_artifact_size",
            goal="Check local model artifact size",
            quality_scenarios=["card.edge_deployment_profile-qas_001"],
            measurement=LocalObjectSize(),
            validator=Real.less_or_equal_to(150.0, unit=Units.megabyte),
        ),
        TestCase(
            identifier="local_process_memory_utilization",
            goal="Check maximum local process memory utilization",
            quality_scenarios=["card.edge_deployment_profile-qas_002"],
            measurement=LocalProcessMemoryUtilization(),
            validator=MemoryStatistics.max_utilization_less_than(
                512.0,
                unit=Units.megabyte,
            ),
        ),
        TestCase(
            identifier="local_process_cpu_utilization",
            goal="Check maximum local process CPU utilization",
            quality_scenarios=["card.edge_deployment_profile-qas_003"],
            measurement=LocalProcessCPUUtilization(),
            validator=CPUStatistics.max_utilization_less_than(75.0),
        ),
    ]
)
spec.save(parents=True, force=True)