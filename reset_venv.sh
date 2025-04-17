#!/usr/bin/env bash
set -e

rm -r -f .venv
python -m venv .venv
poetry install --with dev --all-extras
