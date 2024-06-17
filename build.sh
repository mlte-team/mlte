#!/usr/bin/env bash
cd mlte/frontend/nuxt-app && npm run build
cd ../../../
poetry build

rm docker/deployment/mlte_python-*.whl
cp dist/mlte_python-*.whl docker/deployment/
