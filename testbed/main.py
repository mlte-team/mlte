"""
A simple program for testing functionality during development.
"""

import os
import sys
from resolver import package_root

sys.path.append(package_root())

import mlte
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types import Integer

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    here = os.path.abspath(os.getcwd())
    here = os.path.join(here, "deleteme")

    mlte.set_model("FakeModel", "0.0.1")
    mlte.set_artifact_store_uri(f"local://{here}")

    m = LocalObjectSize("model size")
    r = m(__file__)
    print(r)

    r.save()
    r: Integer = Integer.load("model size")
    print(r)

    v = r.less_than(500)
    print(v)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
