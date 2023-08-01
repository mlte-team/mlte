"""
mlte/cli/cli.py

Top-level command line interface.
"""

import sys
import argparse

import mlte.store.main as server
import mlte.frontend as frontend
from mlte.store.core.config import settings

# CLI exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The global name of the program
_PROGRAM_NAME = "mlte"

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
    _attach_frontend(subparser)

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
        default=settings.APP_HOST,
        help=f"The host address to which the server binds (default: {settings.APP_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(settings.APP_PORT),
        help=f"The port on which the server listens (default: {settings.APP_PORT})",
    )
    parser.add_argument(
        "--backend-uri",
        type=str,
        required=True,
        help="The URI for the backend store.",
    )


def _attach_frontend(
    subparser,
):
    """Attach the frontend subparser to the base parser."""
    parser = subparser.add_parser(
        "frontend", help="Run an instance of the MLTE Frontend."
    )
    parser.set_defaults(func=frontend.run_frontend)


# -----------------------------------------------------------------------------
# Entry Point
# -----------------------------------------------------------------------------


def run():
    """Parse command line arguments and execute specified script."""
    parser = _prepare_parser()
    args = vars(parser.parse_args())

    try:
        run = args.pop("func")
        return run(**args)
    except KeyError:
        parser.print_help()
        return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(run())
