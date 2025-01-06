#!/usr/bin/env bash

MODEL="OxfordFlower"
VERSION="0.0.1"

source copy_nc.sh

# Set env vars to not use a relational DB, but a file store, and point to the one here.
export STORE_TYPE=fs
export HOST_FS_STORE="../../demo/scenarios/store"

# We will use dockerized versions of frontend and backend. This will also build them if needed.
cd ../../docker/deployment
source rebuild_and_restart.sh

source stop.sh
cd ../../demo/scenarios
