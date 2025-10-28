#!/usr/bin/env bash

# Ensure everything stops if there is a failure in one of the commands.
set -e

DOCKER_FOLDER=../docker/deployment

# Function to stop env.
function cleanup() {
    echo "Cleaning up..."
    (cd $DOCKER_FOLDER && source stop.sh)
    exit 130
}

# Set up cleanup function to be called if Ctrl+C is used.
trap cleanup SIGINT

# Needed to copy sample cards.
cp -r ./sample_store ./store

# Set env vars to not use a relational DB, but a file store, and point to the one here.
export STORE_TYPE=fs
export HOST_FS_STORE="../../demo/store"

# We will use dockerized versions of frontend and backend. This will also build them if needed.
(cd $DOCKER_FOLDER && source rebuild_and_restart.sh)

# Unlikely we'll get there, but explicitly call cleanup if the running server scripts stopped for another reason.
cleanup
