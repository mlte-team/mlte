"""
A simple program for testing functionality during development.
"""

import sys
import time
import threading
import subprocess
from resolver import package_root

sys.path.append(package_root())

from mlte.report import Report, Dataset, User, UseCase, Limitation, render

from mlte.suite import Suite, SuiteReport
from mlte.property.costs import (
    StorageCost,
    TrainingComputeCost,
    TrainingMemoryCost,
)

from mlte.measurement import bind
from mlte.measurement.utility import concurrently, flatten
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


def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "ProjectName"
    report.metadata.authors = ["Foo", "Bar"]
    report.metadata.source_url = "https://github.com/mlte-team"
    report.metadata.artifact_url = "https://github.com/mlte-team"
    report.metadata.timestamp = f"{int(time.time())}"

    report.model_details.name = "ModelName"
    report.model_details.overview = "Model overview."
    report.model_details.documentation = "Model documentation."

    report.model_specification.domain = "ModelDomain"
    report.model_specification.architecture = "ModelArchitecture"
    report.model_specification.input = "ModelInput"
    report.model_specification.output = "ModelOutput"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "Description"),
        Dataset("Dataset1", "https://github.com/mlte-team", "Description."),
    ]

    report.considerations.users = [
        User("User0", "User description 0."),
        User("User1", "User description 1."),
    ]
    report.considerations.use_cases = [
        UseCase("UseCase0", "Use case description 0."),
        UseCase("UseCase1", "Use case description 1."),
    ]
    report.considerations.limitations = [
        Limitation(
            "Limitation0",
            """
            Limitation 0 description is defined in a block, multiline string.
            """,
        ),
        Limitation(
            "Limitation1",
            """
            Limitation 1 description is defined in a block, multiline string.
            """,
        ),
    ]
    return report


def build_suite() -> SuiteReport:
    report = build_report()

    suite = Suite(
        "MySuite", StorageCost(), TrainingComputeCost(), TrainingMemoryCost()
    )

    local_size = bind(
        LocalObjectSize().with_validator_size_not_greater_than(threshold=54000),
        suite.get_property("StorageCost"),
    )
    local_cpu = bind(
        LocalProcessCPUUtilization().with_validator_max_utilization_not_greater_than(
            threshold=0.85
        ),
        suite.get_property("TrainingComputeCost"),
    )
    local_mem = bind(
        LocalProcessMemoryConsumption().with_validator_max_consumption_not_greater_than(
            threshold=8192
        ),
        suite.get_property("TrainingMemoryCost"),
    )

    size_result = local_size.validate("test/")

    prog = spin_for(5)
    results = concurrently(
        lambda: local_cpu.validate(prog.pid),
        lambda: local_mem.validate(prog.pid),
    )

    report = suite.collect(*flatten(size_result, results))
    return report


def main() -> int:
    report = build_report()
    report.suite = build_suite()

    html = report.to_html()
    render(html)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
