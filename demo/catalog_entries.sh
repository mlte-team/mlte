#!/usr/bin/env bash
# Build mode: Converts demo evidence notebooks into scripts, and adds or updates them in the sample test catalog
# Check mode: Checks that all sample test catalog entries are updated

if [ "$1" != "build" ] && [ "$1" != "check" ]; then
    echo "Invalid mode."
    exit 1
fi

for notebook_file in ./scenarios/*ipynb
do
    NAME=${notebook_file##*./scenarios/}
    if [[ "${NAME:0:1}" == "2" && "${NAME:1:1}" == [a-z] ]]; then
        if [[ "$1" == "build" ]]; then
            python catalog_entries.py build $notebook_file
        elif [[ "$1" == "check" ]]; then
            python catalog_entries.py check $notebook_file
            if [[ $? == 1 ]]; then
                exit $?
            fi
        fi
    fi
done