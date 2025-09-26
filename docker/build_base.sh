#!/usr/bin/env bash
set -e

(cd .. && docker build -t mlte-python . -f docker/Dockerfile.python)
(cd .. && docker build -t mlte-frontend-env --target frontend-env . -f docker/Dockerfile.frontend)
(cd .. && docker build -t mlte-frontend-build --target frontend-build . -f docker/Dockerfile.frontend)
