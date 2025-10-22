#!/usr/bin/env bash
# Build mode: Converts demo evidence notebooks into scripts, and adds or updates them in the sample test catalog
# Check mode: Checks that all sample test catalog entries are updated

if [ "$1" != "build" ] && [ "$1" != "check" ]; then
    echo "Invalid mode."
    exit 1
fi

for file in ./scenarios/*ipynb
do
    NAME=${file##*./scenarios/}
    if [[ "${NAME:0:1}" == "2" && "${NAME:1:1}" == [a-z] ]]; then
        jupyter nbconvert --to script $file --output-dir conversions/scenarios
    fi
done

for file in ./conversions/scenarios/*.py
do
    if [[ "$1" == "build" ]]; then
        python catalog_entries.py build $file
    elif [[ "$1" == "check" ]]; then
        python catalog_entries.py check $file
        if [[ $? == 1 ]]; then
            exit $?
        fi
    fi
done
