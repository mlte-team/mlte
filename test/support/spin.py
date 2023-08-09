"""
test/support/spin.py

Dummy program to produce work.
"""

import argparse
import sys
import time

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_arguments() -> int:
    """
    Parse commandline arguments.
    :return The number of seconds to run
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("runtime", type=int, help="Program runtime in seconds.")
    args = parser.parse_args()
    return int(args.runtime)


def sleep():
    """Sleep."""
    time.sleep(1)


def work():
    """Perform arbitrary work."""
    data = {}
    char = [chr(v) for v in range(ord("a"), ord("z") + 1)]
    for i in range(10000):
        data[i] = char[i % len(char)]


def spin(runtime: int):
    """
    Spin for specified time period.
    :param runtime The number of seconds to run
    """
    start = time.time()
    while int(time.time() - start) < runtime:
        work()
        sleep()


def main() -> int:
    runtime = parse_arguments()
    try:
        spin(runtime)
    except Exception:
        return EXIT_FAILURE
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
