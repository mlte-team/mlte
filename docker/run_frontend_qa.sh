#!/usr/bin/env bash
set -e

# Build python dockerfile and QA dockerfile
(bash build_base.sh)
(cd .. && docker build -t mlte-frontend-qa . -f docker/Dockerfile.frontend_qa)

docker run --rm \
    -v "$(pwd)/../mlte:/mnt/app/mlte" \
    --tmpfs /mnt/app/node_modules \
    mlte-frontend-qa "$@"