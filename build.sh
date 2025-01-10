#!/usr/bin/env bash
rm dist/mlte_python-*.whl
rm dist/mlte_python-*.gz

cd mlte/frontend/nuxt-app && npm run build
cd ../../../
poetry build

poetry run twine check dist/*
