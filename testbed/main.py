"""
testbed/main.py

A simple program for testing functionality during development.
"""

import os
import sys

from resolver import package_root

sys.path.append(package_root())

from mlte.negotiation.artifact import NegotiationCard
from mlte.session import set_context, set_store

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    store_path = os.path.join(os.getcwd(), "store")
    os.makedirs(store_path, exist_ok=True)

    set_context("ns", "IrisClassifier", "0.0.1")
    set_store(f"local://{store_path}")

    card = NegotiationCard()
    card.save(force=True, parents=True)

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
