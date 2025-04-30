#!/usr/bin/env bash

MODEL="OxfordFlower"
VERSION="0.0.1"

# Function to stop env.
function cleanup() {
    echo "Cleaning up..."
    source stop.sh
    cd ../../demo/scenarios
    exit 130
}

# Set up cleanup function to be called if Ctrl+C is used.
trap cleanup SIGINT

# Needed to copy sample card.
source copy_nc.sh

# Set env vars to not use a relational DB, but a file store, and point to the one here.
export STORE_TYPE=fs
export HOST_FS_STORE="../../demo/scenarios/store"

# We will use dockerized versions of frontend and backend. This will also build them if needed.
cd ../../docker/deployment
source rebuild_and_restart.sh

# Unlikely we'll get there, but explicitly call cleanup if the running server scripts stopped for another reason.
cleanup
