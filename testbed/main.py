"""
A simple program for testing functionality during development.
"""

import sys
import json
import threading
import subprocess
from resolver import package_root

sys.path.append(package_root())

from mlte.suites import Suite

from mlte.properties.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost,
)

from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.memory import LocalProcessMemoryConsumption

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def spin_for(seconds: int):
    """Run the spin.py program for `seconds`."""
    prog = subprocess.Popen(["python", "test/support/spin.py", f"{seconds}"])
    thread = threading.Thread(target=lambda: prog.wait())
    thread.start()
    return prog


def main() -> int:
    suite = Suite(
        "MySuite", StorageCost(), TrainingComputeCost(), TrainingMemoryCost()
    )
    suite.save("tmp/suite.json")

    suite = Suite.from_file("tmp/suite.json")

    # local_size = LocalObjectSize().with_validator_size_not_greater_than(
    #     threshold=54000
    # )
    # local_cpu = LocalProcessCPUUtilization().with_validator_max_utilization_not_greater_than(
    #     threshold=0.85
    # )
    # local_mem = LocalProcessMemoryConsumption().with_validator_max_consumption_not_greater_than(
    #     threshold=8192
    # )

    # size_result = local_size.validate("test/")

    # prog = spin_for(5)
    # cpu_result = local_cpu.validate(prog.pid)

    # prog = spin_for(5)
    # mem_result = local_mem.validate(prog.pid)

    # data = suite.collect(size_result, cpu_result, mem_result)
    # print(json.dumps(data))

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
