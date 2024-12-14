#!/usr/bin/env bash

# Remove everything from temp stores to avoid outdated data.
rm -r ./store/models
mkdir -p ./store/models

poetry run pytest --nbmake ./demo/simple/negotiation.ipynb
poetry run pytest --nbmake ./demo/simple/requirements.ipynb
poetry run pytest --nbmake ./demo/simple/evidence.ipynb
poetry run pytest --nbmake ./demo/simple/report.ipynb
