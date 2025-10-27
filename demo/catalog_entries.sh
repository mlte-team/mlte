#!/usr/bin/env bash
# First CLI param is the mode, build or check, the rest of the params are the demo folders to build or check
# Build mode: Converts demo evidence notebooks into scripts, and adds or updates them in the sample test catalog
# Check mode: Checks that all sample test catalog entries are updated

MODE="$1"

if [ $MODE != "build" ] && [ $MODE != "check" ]; then
    echo "Invalid mode."
    exit 1
fi

# Take the mode param out of the list of params, leaving it just a as a list of the demos
shift

DEMOS=$@
for demo in ${DEMOS[@]}
do
    for notebook_file in ${demo}/*ipynb
    do
        # Get the file name without the demo path prepended
        NAME=${notebook_file##*$demo/}
        # Check if the first character of the path is a 2, and the second is a lowercase letter
        #   This is the naming format for QAC demos that will be enforced so we can identify them here
        if [[ "${NAME:0:1}" == "2" && "${NAME:1:1}" == [a-z] ]]; then
            if [[ $MODE == "build" ]]; then
                python catalog_entries.py build $notebook_file
            elif [[ $MODE == "check" ]]; then
                python catalog_entries.py check $notebook_file
                if [[ $? == 1 ]]; then
                    exit $?
                fi
            fi
        fi
    done
done