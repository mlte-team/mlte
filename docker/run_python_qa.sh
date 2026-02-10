#!/usr/bin/env bash
set -e

# Build python dockerfile and QA dockerfile
(cd .. && docker build -t mlte-python . -f docker/Dockerfile.python)
(cd .. && docker build -t mlte-python-qa . -f docker/Dockerfile.python_qa)

docker run --rm \
    -e GIT_DISCOVERY_ACROSS_FILESYSTEM=1 \
    -v "$(pwd)/../mlte:/mnt/app/mlte" \
    -v "$(pwd)/../demo:/mnt/app/demo" \
    -v "$(pwd)/../docs:/mnt/app/docs" \
    -v "$(pwd)/../test:/mnt/app/test" \
    -v "$(pwd)/../tools:/mnt/app/tools" \
    mlte-python-qa "$1"