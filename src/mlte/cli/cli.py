"""
cli/cli.py

Top-level command line interface.
"""

import sys
import argparse

import mlte.store.main as server

# CLI exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The global name of the program
_PROGRAM_NAME = "mlte"

# The deafult host address to which the server binds
_DEFAULT_HOST = "localhost"
# The default port on which the server listens
_DEFAULT_PORT = 8080

# -----------------------------------------------------------------------------
# Parsing Setup
# -----------------------------------------------------------------------------


def _prepare_parser():
    """Prepare the base parser."""

    # The base parser
    base_parser = argparse.ArgumentParser(prog=_PROGRAM_NAME)

    # Attach subparsers
    subparser = base_parser.add_subparsers(help="Subcommands:")
    _attach_store(subparser)

    return base_parser


def _attach_store(
    subparser,
):
    """Attach the artifact store subparser to the base parser."""
    parser = subparser.add_parser(
        "store", help="Run an instance of the MLTE artifact store."
    )
    parser.set_defaults(func=server.run)
    parser.add_argument(
        "--host",
        type=str,
        default=_DEFAULT_HOST,
        help=f"The host address to which the server binds (default: {_DEFAULT_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=_DEFAULT_PORT,
        help=f"The port on which the server listens (default: {_DEFAULT_PORT})",
    )
    parser.add_argument(
        "--backend-uri",
        type=str,
        required=True,
        help="The URI for the backend store.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output."
    )


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------


def run():
    """Parse command line arguments and execute specified script."""
    parser = _prepare_parser()
    args = vars(parser.parse_args())

    run = args.get("func")
    if run:
        return run(**args)
    else:
        parser.print_help()
        return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(run())
