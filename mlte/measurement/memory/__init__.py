from .local_process_memory_consumption import (
    LocalProcessMemoryConsumption,
    MemoryStatistics
)

from .nvidia_gpu_memory_consumption import (
    LocalNvidiaGPUMemoryConsumption,
    NvidiaGPUMemoryStatistics
)

# TODO(Kyle): Find a more elegant way to do this
__all__ = ["LocalProcessMemoryConsumption", "MemoryStatistics",
           "LocalNvidiaGPUMemoryConsumption", "NvidiaGPUMemoryStatistics"]
