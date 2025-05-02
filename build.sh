#!/usr/bin/env bash

# Stop on error.
set -e

# Cleanup.
rm -r -f dist
mkdir dist

# Build frontend as static website.
(cd mlte/frontend/nuxt-app && npm run build)

# Validate pyproject.toml and lock file for consistency.
poetry check

# Do the actual sdist and wheel creation.
poetry build

# Check if the description/readme in the created packages are ok for PyPi.
poetry run twine check dist/*
