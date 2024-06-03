#!/usr/bin/env bash
cd mlte/frontend/nuxt-app && npm run build
cd ../../../
poetry build
cp dist/mlte_python-*.whl docker/dist
