#!/usr/bin/env bash
# Converts demo evidence notebooks into scripts, and adds or updates them in the sample test catalog

for file in ./scenarios/*ipynb
do
    NAME=${file##*./scenarios/}
    if [[ "${NAME:0:1}" == "2" && "${NAME:1:1}" == [a-z] ]]; then
        jupyter nbconvert --to script $file --output-dir conversions/scenarios
    fi
done

for file in ./conversions/scenarios/*.py
do
    python build_entries.py $file
done