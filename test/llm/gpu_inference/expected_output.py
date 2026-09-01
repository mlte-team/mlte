spec = TestSuite(
    test_cases=[
        TestCase(
            identifier="gpu_memory_utilization",
            goal="Check NVIDIA GPU memory utilization",
            quality_scenarios=["card.gpu_inference_profile-qas_001"],
            measurement=NvidiaGPUMemoryUtilization(),
            validator=NvidiaGPUMemoryStatistics.max_utilization_less_than(
                10.0,
                unit=Units.gigabyte,
            ),
        ),
        TestCase(
            identifier="gpu_power_utilization",
            goal="Check NVIDIA GPU power utilization",
            quality_scenarios=["card.gpu_inference_profile-qas_002"],
            measurement=NvidiaGPUPowerUtilization(),
            validator=NvidiaGPUPowerStatistics.average_utilization_less_than(
                250.0
            ),
        ),
        TestCase(
            identifier="gpu_inference_cpu_utilization",
            goal="Check local CPU utilization during GPU inference",
            quality_scenarios=["card.gpu_inference_profile-qas_003"],
            measurement=LocalProcessCPUUtilization(),
            validator=CPUStatistics.max_utilization_less_than(60.0),
        ),
    ]
)
spec.save(parents=True, force=True)
