"""
A simple program for testing functionality during development.
"""

import sys
from resolver import package_root
sys.path.append(package_root())

from mlte.properties.cpu import LocalProcessCPUUtilization

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def main() -> int:
    p = LocalProcessCPUUtilization()
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
