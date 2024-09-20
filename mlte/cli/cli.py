"""
mlte/cli/cli.py

Top-level command line interface.
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from importlib.metadata import PackageNotFoundError, version

import mlte.backend.main as backend
import mlte.frontend as frontend
from mlte.backend.core.config import settings as backend_settings
from mlte.frontend.config import settings as frontend_settings

# CLI exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The global name of the program
_PROGRAM_NAME = "mlte"

# The name of the package.
_PACKAGE_NAME = "mlte-python"

# -----------------------------------------------------------------------------
# Parsing Setup
# -----------------------------------------------------------------------------


def _get_version() -> str:
    """Gets the version of the currently installed MLTE."""
    try:
        return version(_PACKAGE_NAME)
    except PackageNotFoundError:
        return "<mlte is not installed as a package.>"


def _prepare_parser():
    """Prepare the base parser."""

    # The base parser
    base_parser = argparse.ArgumentParser(prog=_PROGRAM_NAME)

    # Version flag.
    base_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {_get_version()}",
    )

    # Attach subparsers
    subparser = base_parser.add_subparsers(help="Subcommands:")
    for attach_to in [_attach_backend_parser, _attach_frontend_parser]:
        attach_to(subparser)
    return base_parser


def _attach_backend_parser(
    subparser: argparse._SubParsersAction[argparse.ArgumentParser],
):
    """Attach the artifact store subparser to the base parser."""
    parser: argparse.ArgumentParser = subparser.add_parser(
        "backend", help="Run an instance of the MLTE artifact store."
    )
    parser.set_defaults(func=backend.run)

    # Additional arguments.
    parser.add_argument(
        "--host",
        type=str,
        default=backend_settings.BACKEND_HOST,
        help=f"The host address to which the server binds (default: {backend_settings.BACKEND_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(backend_settings.BACKEND_PORT),
        help=f"The port on which the server listens (default: {backend_settings.BACKEND_PORT})",
    )
    parser.add_argument(
        "--store-uri",
        type=str,
        default=backend_settings.STORE_URI,
        help=f"The URI for the backend store (default: {backend_settings.STORE_URI}).",
    )
    parser.add_argument(
        "--catalog-uris",
        type=json.loads,
        default=backend_settings.CATALOG_URIS,
        help=f"A JSON string with a dictionary of URI for the backend catalog stores to usestore (default: {backend_settings.CATALOG_URIS}).",
    )
    parser.add_argument(
        "--allowed-origins",
        nargs="*",
        default=backend_settings.ALLOWED_ORIGINS,
        help=f"A list of allowed CORS origins (default: {backend_settings.ALLOWED_ORIGINS})",
    )
    parser.add_argument(
        "--jwt-secret",
        type=str,
        default=backend_settings.JWT_SECRET_KEY,
        help="A secret random string key used to sign tokens",
    )


def _attach_frontend_parser(
    subparser: argparse._SubParsersAction[argparse.ArgumentParser],
):
    """Attach the frontend UI subparser to the base parser."""
    parser: argparse.ArgumentParser = subparser.add_parser(
        "ui", help="Run an instance of the MLTE frontend user interface."
    )
    parser.set_defaults(func=frontend.run_frontend)

    # Additional arguments.
    parser.add_argument(
        "--host",
        type=str,
        default=frontend_settings.FRONTEND_HOST,
        help=f"The host address to which the frontend server binds (default: {frontend_settings.FRONTEND_HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(frontend_settings.FRONTEND_PORT),
        help=f"The port on which the frontend server listens (default: {frontend_settings.FRONTEND_PORT})",
    )


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
    except Exception:
        traceback.print_exc()
        return EXIT_FAILURE


if __name__ == "__main__":
    sys.exit(run())
