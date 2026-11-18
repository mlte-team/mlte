#!/usr/bin/env bash
set -e

NODE_VERSION="$(mise exec -- node -p 'process.versions.node')"
UV_VERSION="$(mise exec -- uv --version | awk '{print $2}')"

(cd .. && docker build -t mlte-python . -f docker/Dockerfile.python --build-arg UV_VERSION="$UV_VERSION")
(cd .. && docker build -t mlte-frontend-env --target frontend-env . -f docker/Dockerfile.frontend --build-arg NODE_VERSION="$NODE_VERSION")
(cd .. && docker build -t mlte-frontend-build --target frontend-build . -f docker/Dockerfile.frontend --build-arg NODE_VERSION="$NODE_VERSION")
