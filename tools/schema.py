"""
tools/schema.py

A tool for generating and vetting MLTE artifact schemas.
"""

from __future__ import annotations

import argparse
import importlib
import json
import logging
import sys
import typing
from pathlib import Path
from typing import Any, Dict

import deepdiff
from pydantic import BaseModel

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The base path for artifact generation
OUTPUT_BASE = Path("schema/artifact")


class ModelImport:
    """A ModelImport describes the module and classname for a MLTE model."""

    def __init__(self, *, path: str, model: str) -> None:
        self.path = path
        """The path to the module in which the model is defined."""

        self.model = model
        """The identifier for the model of interest."""

    def resolve(self) -> BaseModel:
        """Resolve the import to a class."""
        return typing.cast(
            BaseModel, getattr(importlib.import_module(self.path), self.model)
        )


class Config:
    """A configuration for a shchema task."""

    def __init__(self, *, model: ModelImport, output_path: str) -> None:
        self.model = model
        """The the model import descriptor."""

        self.output_path = OUTPUT_BASE / output_path / "schema.json"
        """The path to which the model is dumped."""

    def generate(self) -> Dict[str, Any]:
        """Generate the schema for the configuration."""
        klass = self.model.resolve()
        return klass.model_json_schema()

    def __str__(self) -> str:
        return f"{self.model.model} @ {self.output_path}"


# The global collection of configurations
CONFIGS = [
    Config(
        model=ModelImport(
            path="mlte.negotiation.model", model="NegotiationCardModel"
        ),
        output_path="negotiation/v0.0.1",
    ),
    Config(
        model=ModelImport(path="mlte.value.model", model="ValueModel"),
        output_path="value/v0.0.1",
    ),
    Config(
        model=ModelImport(path="mlte.spec.model", model="SpecModel"),
        output_path="spec/v0.0.1",
    ),
    Config(
        model=ModelImport(
            path="mlte.validation.model", model="ValidatedSpecModel"
        ),
        output_path="validated/v0.0.1",
    ),
]

# -----------------------------------------------------------------------------
# Argument Parsing
# -----------------------------------------------------------------------------


def prepare_parser():
    """Prepare the base parser."""

    # The base parser
    base_parser = argparse.ArgumentParser()
    subparser = base_parser.add_subparsers(help="Subcommands:")

    gen_parser: argparse.ArgumentParser = subparser.add_parser(
        "generate", help="Generate MLTE artifact schemas."
    )
    gen_parser.set_defaults(func=generate)
    gen_parser.add_argument(
        "mlte_path", type=Path, help="The path to the MLTE package root."
    )
    gen_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )

    vet_parser: argparse.ArgumentParser = subparser.add_parser(
        "vet", help="Vet MLTE artifact schemas."
    )
    vet_parser.set_defaults(func=vet)
    vet_parser.add_argument(
        "mlte_path", type=Path, help="The path to the MLTE package root."
    )
    vet_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output."
    )

    return base_parser


# -----------------------------------------------------------------------------
# Vet
# -----------------------------------------------------------------------------


def vet_one(config: Config, mlte_path: Path) -> None:
    """
    vet a schema for a MLTE artifact.
    :param config: The configuration for which vetting is performed
    :param mlte_path: The path to the MLTE package root
    """
    path = mlte_path / config.output_path
    if not path.exists():
        raise RuntimeError(f"Not found: {path}")

    logging.info(f"Vetting {config.model.model} with {path}")

    with path.open("r") as f:
        expected = json.load(f)

    diff = deepdiff.DeepDiff(expected, config.generate())
    if not len(diff) == 0:
        raise RuntimeError(f"Schema at {path} is not up to date.")


def vet(mlte_path: Path) -> None:
    """
    Vet MLTE artifacts for updates.
    :param mlte_path: The path to the MLTE package root.
    """
    logging.info(f"vet({mlte_path})")
    for config in CONFIGS:
        vet_one(config, mlte_path)


# -----------------------------------------------------------------------------
# Generate
# -----------------------------------------------------------------------------


def generate_one(config: Config, mlte_path: Path) -> None:
    """
    Generate a schema for a MLTE artifact.
    :param config: The configuration for which generation is performed
    :param mlte_path: The path to the MLTE package root
    """
    path = mlte_path / config.output_path

    dir = path.parent
    if not dir.exists():
        dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Writing {config.model.model} at {path}")

    with open(path, "w") as f:
        json.dump(config.generate(), f, indent=2)


def generate(mlte_path: Path) -> None:
    """
    Generate schemas for MLTE artifacts.
    :param mlte_path: The path to the MLTE package root.
    """
    logging.info(f"generate({mlte_path})")
    for config in CONFIGS:
        generate_one(config, mlte_path)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main() -> int:
    parser = prepare_parser()
    args = vars(parser.parse_args())
    logging.basicConfig(
        level=logging.DEBUG if args.pop("verbose") else logging.ERROR
    )

    try:
        run = args.pop("func")
        run(**args)
    except KeyError:
        parser.print_help()
        return EXIT_SUCCESS

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
