#!/usr/bin/env bash
rm dist/mlte_python-*.whl
rm dist/mlte_python-*.gz

poetry check
poetry build
