"""
testbed/main.py

A simple program for testing functionality during development.
"""

import os
import sys
from resolver import package_root

sys.path.append(package_root())

import mlte
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types import Integer
import mlte.api as api

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    here = os.path.abspath(os.getcwd())
    here = os.path.join(here, "deleteme")
    uri = f"local://{here}"

    mlte.set_model("FakeModel", "0.0.1")
    mlte.set_artifact_store_uri(uri)

    m = LocalObjectSize("file size")
    r: Integer = m.evaluate(os.path.abspath(__file__))
    r.save()

    result = api.read_value(uri, "FakeModel", "0.0.1", "file size")
    print(result)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
