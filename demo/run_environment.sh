#!/usr/bin/env bash

# Needed to copy sample cards.
cp -r ./sample_store ./store

# Point to our demo local store and run the environment.
HOST_FS_STORE="$(pwd -P)/store"
(cd ../ && source ./run_environment.sh "${HOST_FS_STORE}")
