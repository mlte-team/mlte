#!/usr/bin/env bash

# Build base images (backend is the one actually needed).
(cd ../../docker && bash build.sh)

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="mlte-backend-demo"

# Build demo image.
docker build -f "$SCRIPT_DIR/Dockerfile" -t "$IMAGE_NAME" "$PARENT_DIR"
