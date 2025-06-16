#!/usr/bin/env bash
set -e

(cd .. && docker build -t mlte-python . -f docker/Dockerfile.python)
(cd .. && docker build -t mlte-node . -f docker/Dockerfile.node)
