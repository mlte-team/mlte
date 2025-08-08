#!/usr/bin/env bash

MODEL="OxfordFlower"

# Copy sample negotiation card to our working store space. Create folders if needed.
mkdir -p store/models/$MODEL
cp ../sample_store/models/$MODEL/*.json ./store/models/$MODEL
