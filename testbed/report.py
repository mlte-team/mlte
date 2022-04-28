"""
Small testbed for report generation.
"""

import sys
import json
import time
from resolver import package_root

sys.path.append(package_root())

from mlte.report import *
from mlte.suites import SuiteReport

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    report = Report()
    report.metadata.project_name = "ProjectName"
    report.metadata.authors = ["Foo", "Bar"]
    report.metadata.source_url = "https://github.com/mlte-team"
    report.metadata.artifacts_url = "https://github.com/mlte-team"
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
        User("User description 0."),
        User("User description 1."),
    ]
    report.considerations.use_cases = [
        UseCase("Use case description 0."),
        UseCase("Use case description 1."),
    ]
    report.considerations.limitations = [
        Limitation("Limitation description 0."),
        Limitation("Limitation description 1."),
    ]

    report.suite = SuiteReport({})

    print(json.dumps(report.json(), indent=2))

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
