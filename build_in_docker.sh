#!/usr/bin/env bash

# Stop on error.
set -e -x

# Cleanup.
rm -r -f dist
mkdir dist

# Build dist image, which will build the package.
(cd docker && bash build_base.sh)
docker build -t mlte-dist . -f docker/Dockerfile.dist

# Start a container from that image, and copy the package out.
docker run --rm -v ./dist:/dist mlte-dist bash -c "cp /mnt/app/dist/*.* /dist/"
