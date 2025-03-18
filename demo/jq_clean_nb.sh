#!/usr/bin/env bash

# This command cleans a notebook, removing output and temp metadata.
# NOTE: this requires jq to be installed in the system.
jq --indent 1 \
    '
    (.cells[] | select(has("outputs")) | .outputs) = []
    | (.cells[] | select(has("execution_count")) | .execution_count) = null
    | .metadata.kernelspec = {"display_name": ".venv", "language":"python", "name": "python3"}
    | .cells[].metadata = {}
    ' "${1}" > OUT.tmp && mv OUT.TMP "${1}"
