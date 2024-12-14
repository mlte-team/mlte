#!/usr/bin/env bash
CURR_FOLDER="./demo/simple"

# Remove everything from temp stores to avoid outdated data.
rm -r ${CURR_FOLDER}/store/models
mkdir -p ${CURR_FOLDER}/store/models

poetry run pytest --nbmake ${CURR_FOLDER}/negotiation.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/requirements.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/evidence.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/report.ipynb
