#!/usr/bin/env bash
CURR_FOLDER="./demo/simple"

# Remove everything from temp stores to avoid outdated data.
rm -r ${CURR_FOLDER}/store/models
mkdir -p ${CURR_FOLDER}/store/models

# Copy sample negotiation card to store.
source copy_nc.sh

poetry run pytest --nbmake ${CURR_FOLDER}/1_negotiation.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2_requirements.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/3_evidence.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/4_report.ipynb
