#!/usr/bin/env bash

# This command cleans a notebook, removing output and temp metadata.
# NOTE: this requires jq to be installed in the system.
# More specifically, this command:
# - Clears all cell outputs
# - Clears all cell metadata
# - Clears all execution_count fields
# - Sets kernelspec to a default set of values, to avoid constantly getting it updated due to the last user's environment
# - Sets language version ot a default value, to avoid constantly getting it updated due to the last users's environment
jq --indent 1 \
    '
    (.cells[] | select(has("outputs")) | .outputs) = []
    | .cells[].metadata = {}
    | (.cells[] | select(has("execution_count")) | .execution_count) = null
    | .metadata.kernelspec = {"display_name": ".venv", "language":"python", "name": "python3"}
    | .metadata.language_info.version = "3.12.11"    
    ' "${1}" > OUT.tmp && mv OUT.TMP "${1}"
