#!/usr/bin/env bash

# Stop on error.
set -e

# Cleanup.
rm -r -f dist
mkdir dist

# Build frontend as static website.
(cd mlte/frontend/nuxt-app && npm run build)

# Do the actual sdist and wheel creation.
uv build

# Check if the description/readme in the created packages are ok for PyPi.
uv run twine check dist/*
