#!/usr/bin/env bash

MODEL="OxfordFlower"
VERSION="0.0.1"

# Copy sample negotiation card to our working store space. Create folders if needed.
mkdir -p store/models/$MODEL/$VERSION
cp ../sample_store/models/$MODEL/$VERSION/*.json ./store/models/$MODEL/$VERSION

# Set env vars to not use a relational DB, but a file store.
export BACKEND_ENVFILE=../../demo/scenarios/.env.backend.demo
export COMPOSE_PROFILES=

# We will use dockerized versions of frontend and backend. This will also build them if needed.
cd ../../docker/deployment
source rebuild_and_restart.sh

source stop.sh
cd ../../demo/scenarios
