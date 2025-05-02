#!/usr/bin/env bash
rm -r dist
mkdir dist

cd mlte/frontend/nuxt-app && npm run build
cd ../../../
poetry check
poetry build

poetry run twine check dist/*
