#!/usr/bin/env bash
# Starts up a MLTE environment with a local file store. 
# The folder can be provided as an argument, or it will default to ./store.

# Ensure everything stops if there is a failure in one of the commands.
set -e

DOCKER_FOLDER=./docker/deployment

# Function to stop env.
function cleanup() {
    echo "Cleaning up..."
    (cd $DOCKER_FOLDER && source stop.sh)
    exit 130
}

# Set up cleanup function to be called if Ctrl+C is used.
trap cleanup SIGINT

# Get store from argument and set it, or default to ./store if not provided.
export HOST_FS_STORE="${1:-$(pwd -P)/store}"

# Set env vars to not use a relational DB, but a file store, and point to the provided one.
export STORE_TYPE=fs
echo "Mounting store on local absolute path ${HOST_FS_STORE}"

# We will use dockerized versions of frontend and backend. This will also build them if needed.
(cd $DOCKER_FOLDER && source rebuild_and_restart.sh)

# Explicitly call cleanup when the running server scripts stop.
cleanup
