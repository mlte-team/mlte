#!/usr/bin/env bash

MODEL="OxfordFlower"
VERSION="0.0.1"

# Copy sample negotiation card to our working store space. Create folders if needed.
mkdir -p store/models/$MODEL/$VERSION
cp ../sample_store/models/$MODEL/$VERSION/*.json ./store/models/$MODEL/$VERSION
