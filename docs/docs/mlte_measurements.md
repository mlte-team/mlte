# MLTE Measurements

The following are specific built-in measurement classes provided by MLTE:

- LocalProcessCPUUtilization
    - CPU utilization measurement for local training processes.
    - Returns custom evidence in the form of a CPUStatistics object.
- LocalProcessMemoryConsumption
    - Memory consumption measurement for local training processes.
    - Returns custom evidence in the form of a MemoryStatistics object.
- LocalObjectSize
    - Measure the size of a locally-stored object.
- NvidiaGPUMemoryConsumption
    - Measures the amount memory being used per-GPU during an experiment.
    - Returns custom evidence in the form of an NvidiaGPUMemoryStatistics object.
    - Requires a CUDA-capable NVIDIA GPU to be used, as well as the CUDA Toolkit (including the NVML library) to be installed. 

The following are more generic measurement classes that can be used directly, or extended:

- ExternalMeasurement
    - Generic class to use external functions to perform measurments.
    - Wraps results in MLTE-compatible evidence types.
- ImportMeasurement
    - Simple JSON importer class for evidence from external measurements.
    - Wraps results in a MLTE Opaque (dict-like) evidence type.
- ProcessMeasurement
    - Base class for measurements that require launching an external process.

For more information on `MLTE` measurements, see the [measurement](reference/measurement/measurement.md) section of the API Reference.
